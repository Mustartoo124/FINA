"""
Tool for querying Vertex AI RAG corpora and retrieving relevant information.
"""

import logging
import re 
from typing import List, Dict, Union

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ..config import (
    DEFAULT_DISTANCE_THRESHOLD,
    DEFAULT_TOP_K,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_EMBEDDING_REQUESTS_PER_MIN,
    DEFAULT_EMBEDDING_MODEL,
)
from .utils import check_corpus_exists, get_corpus_resource_name

def add_data(
    corpus_name: str,
    paths: List[str],
    tool_context: ToolContext,
) -> dict:
    """
    Add new data sources to a Vertex AI RAG corpus.

    Args:
        corpus_name (str): The name of the corpus to add data to. If empty, the current corpus will be used.
        paths (List[str]): List of URLs or GCS paths to add to the corpus.
                          Supported formats:
                          - Google Drive: "https://drive.google.com/file/d/{FILE_ID}/view"
                          - Google Docs/Sheets/Slides: "https://docs.google.com/{type}/d/{FILE_ID}/..."
                          - Google Cloud Storage: "gs://{BUCKET}/{PATH}"
                          Example: ["https://drive.google.com/file/d/123", "gs://my_bucket/my_files_dir"]
        tool_context (ToolContext): The tool context

    Returns:
        dict: Information about the added data and status
    """
    # Check if the corpus exists
    if not check_corpus_exists(corpus_name, tool_context):
        return {
            "status": "error",
            "message": f"Corpus '{corpus_name}' does not exist. Please create it first using the create_corpus tool.",
            "corpus_name": corpus_name,
            "paths": paths,
        }

    # Validate inputs
    if not paths or not all(isinstance(path, str) for path in paths):
        return {
            "status": "error",
            "message": "Invalid paths: Please provide a list of URLs or GCS paths",
            "corpus_name": corpus_name,
            "paths": paths,
        }

    # Pre-process paths to validate and convert Google Docs URLs to Drive format if needed
    validated_paths = []
    invalid_paths = []
    conversions = []

    for path in paths:
        if not path or not isinstance(path, str):
            invalid_paths.append(f"{path} (Not a valid string)")
            continue

        # Check for Google Docs/Sheets/Slides URLs and convert them to Drive format
        docs_match = re.match(
            r"https:\/\/docs\.google\.com\/(?:document|spreadsheets|presentation)\/d\/([a-zA-Z0-9_-]+)(?:\/|$)",
            path,
        )
        if docs_match:
            file_id = docs_match.group(1)
            drive_url = f"https://drive.google.com/file/d/{file_id}/view"
            validated_paths.append(drive_url)
            conversions.append(f"{path} → {drive_url}")
            continue

        # Check for valid Drive URL format
        drive_match = re.match(
            r"https:\/\/drive\.google\.com\/(?:file\/d\/|open\?id=)([a-zA-Z0-9_-]+)(?:\/|$)",
            path,
        )
        if drive_match:
            # Normalize to the standard Drive URL format
            file_id = drive_match.group(1)
            drive_url = f"https://drive.google.com/file/d/{file_id}/view"
            validated_paths.append(drive_url)
            if drive_url != path:
                conversions.append(f"{path} → {drive_url}")
            continue

        # Check for GCS paths
        if path.startswith("gs://"):
            validated_paths.append(path)
            continue

        # If we're here, the path wasn't in a recognized format
        invalid_paths.append(f"{path} (Invalid format)")

    # Check if we have any valid paths after validation
    if not validated_paths:
        return {
            "status": "error",
            "message": "No valid paths provided. Please provide Google Drive URLs or GCS paths.",
            "corpus_name": corpus_name,
            "invalid_paths": invalid_paths,
        }

    try:
        # Get the corpus resource name
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        # Set up chunking configuration
        transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=DEFAULT_CHUNK_SIZE,
                chunk_overlap=DEFAULT_CHUNK_OVERLAP,
            ),
        )

        # Import files to the corpus
        import_result = rag.import_files(
            corpus_resource_name,
            validated_paths,
            transformation_config=transformation_config,
            max_embedding_requests_per_min=DEFAULT_EMBEDDING_REQUESTS_PER_MIN,
        )

        # Set this as the current corpus if not already set
        if not tool_context.state.get("current_corpus"):
            tool_context.state["current_corpus"] = corpus_name

        # Build the success message
        conversion_msg = ""
        if conversions:
            conversion_msg = " (Converted Google Docs URLs to Drive format)"

        return {
            "status": "success",
            "message": f"Successfully added {import_result.imported_rag_files_count} file(s) to corpus '{corpus_name}'{conversion_msg}",
            "corpus_name": corpus_name,
            "files_added": import_result.imported_rag_files_count,
            "paths": validated_paths,
            "invalid_paths": invalid_paths,
            "conversions": conversions,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding data to corpus: {str(e)}",
            "corpus_name": corpus_name,
            "paths": paths,
        }

def create_corpus(
    corpus_name: str,
    tool_context: ToolContext,
) -> dict:
    """
    Create a new Vertex AI RAG corpus with the specified name.

    Args:
        corpus_name (str): The name for the new corpus
        tool_context (ToolContext): The tool context for state management

    Returns:
        dict: Status information about the operation
    """
    # Check if corpus already exists
    if check_corpus_exists(corpus_name, tool_context):
        return {
            "status": "info",
            "message": f"Corpus '{corpus_name}' already exists",
            "corpus_name": corpus_name,
            "corpus_created": False,
        }

    try:
        # Clean corpus name for use as display name
        display_name = re.sub(r"[^a-zA-Z0-9_-]", "_", corpus_name)

        # Configure embedding model
        embedding_model_config = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model=DEFAULT_EMBEDDING_MODEL
            )
        )

        # Create the corpus
        rag_corpus = rag.create_corpus(
            display_name=display_name,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=embedding_model_config
            ),
        )

        # Update state to track corpus existence
        tool_context.state[f"corpus_exists_{corpus_name}"] = True

        # Set this as the current corpus
        tool_context.state["current_corpus"] = corpus_name

        return {
            "status": "success",
            "message": f"Successfully created corpus '{corpus_name}'",
            "corpus_name": rag_corpus.name,
            "display_name": rag_corpus.display_name,
            "corpus_created": True,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating corpus: {str(e)}",
            "corpus_name": corpus_name,
            "corpus_created": False,
        }
    
        
def rag_query(
    corpus_name: str,
    query: str,
    tool_context: ToolContext,
) -> dict:
    """
    Query a Vertex AI RAG corpus with a user question and return relevant information.

    Args:
        corpus_name (str): The name of the corpus to query. If empty, the current corpus will be used.
                          Preferably use the resource_name from list_corpora results.
        query (str): The text query to search for in the corpus
        tool_context (ToolContext): The tool context

    Returns:
        dict: The query results and status
    """
    try:

        # Check if the corpus exists
        if not check_corpus_exists(corpus_name, tool_context):
            return {
                "status": "error",
                "message": f"Corpus '{corpus_name}' does not exist. Please create it first using the create_corpus tool.",
                "query": query,
                "corpus_name": corpus_name,
            }

        # Get the corpus resource name
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        # Configure retrieval parameters
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=DEFAULT_TOP_K,
            filter=rag.Filter(vector_distance_threshold=DEFAULT_DISTANCE_THRESHOLD),
        )

        # Perform the query
        print("Performing retrieval query...")
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=corpus_resource_name,
                )
            ],
            text=query,
            rag_retrieval_config=rag_retrieval_config,
        )

        # Process the response into a more usable format
        results = []
        if hasattr(response, "contexts") and response.contexts:
            for ctx_group in response.contexts.contexts:
                result = {
                    "source_uri": (
                        ctx_group.source_uri if hasattr(ctx_group, "source_uri") else ""
                    ),
                    "source_name": (
                        ctx_group.source_display_name
                        if hasattr(ctx_group, "source_display_name")
                        else ""
                    ),
                    "text": ctx_group.text if hasattr(ctx_group, "text") else "",
                    "score": ctx_group.score if hasattr(ctx_group, "score") else 0.0,
                }
                results.append(result)

        # If we didn't find any results
        if not results:
            return {
                "status": "warning",
                "message": f"No results found in corpus '{corpus_name}' for query: '{query}'",
                "query": query,
                "corpus_name": corpus_name,
                "results": [],
                "results_count": 0,
            }

        return {
            "status": "success",
            "message": f"Successfully queried corpus '{corpus_name}'",
            "query": query,
            "corpus_name": corpus_name,
            "results": results,
            "results_count": len(results),
        }

    except Exception as e:
        error_msg = f"Error querying corpus: {str(e)}"
        logging.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
            "query": query,
            "corpus_name": corpus_name,
        }

def delete_corpus(
    corpus_name: str,
    confirm: bool,
    tool_context: ToolContext,
) -> dict:
    """
    Delete a Vertex AI RAG corpus when it's no longer needed.
    Requires confirmation to prevent accidental deletion.

    Args:
        corpus_name (str): The full resource name of the corpus to delete.
                           Preferably use the resource_name from list_corpora results.
        confirm (bool): Must be set to True to confirm deletion
        tool_context (ToolContext): The tool context

    Returns:
        dict: Status information about the deletion operation
    """
    # Check if corpus exists
    if not check_corpus_exists(corpus_name, tool_context):
        return {
            "status": "error",
            "message": f"Corpus '{corpus_name}' does not exist",
            "corpus_name": corpus_name,
        }

    # Check if deletion is confirmed
    if not confirm:
        return {
            "status": "error",
            "message": "Deletion requires explicit confirmation. Set confirm=True to delete this corpus.",
            "corpus_name": corpus_name,
        }

    try:
        # Get the corpus resource name
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        # Delete the corpus
        rag.delete_corpus(corpus_resource_name)

        # Remove from state by setting to False
        state_key = f"corpus_exists_{corpus_name}"
        if state_key in tool_context.state:
            tool_context.state[state_key] = False

        return {
            "status": "success",
            "message": f"Successfully deleted corpus '{corpus_name}'",
            "corpus_name": corpus_name,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error deleting corpus: {str(e)}",
            "corpus_name": corpus_name,
        }
        
def delete_document(
    corpus_name: str,
    document_id: str,
    tool_context: ToolContext,
) -> dict:
    """
    Delete a specific document from a Vertex AI RAG corpus.

    Args:
        corpus_name (str): The full resource name of the corpus containing the document.
                          Preferably use the resource_name from list_corpora results.
        document_id (str): The ID of the specific document/file to delete. This can be
                          obtained from get_corpus_info results.
        tool_context (ToolContext): The tool context

    Returns:
        dict: Status information about the deletion operation
    """
    # Check if corpus exists
    if not check_corpus_exists(corpus_name, tool_context):
        return {
            "status": "error",
            "message": f"Corpus '{corpus_name}' does not exist",
            "corpus_name": corpus_name,
            "document_id": document_id,
        }

    try:
        # Get the corpus resource name
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        # Delete the document
        rag_file_path = f"{corpus_resource_name}/ragFiles/{document_id}"
        rag.delete_file(rag_file_path)

        return {
            "status": "success",
            "message": f"Successfully deleted document '{document_id}' from corpus '{corpus_name}'",
            "corpus_name": corpus_name,
            "document_id": document_id,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error deleting document: {str(e)}",
            "corpus_name": corpus_name,
            "document_id": document_id,
        }

def get_corpus_info(
    corpus_name: str,
    tool_context: ToolContext,
) -> dict:
    """
    Get detailed information about a specific RAG corpus, including its files.

    Args:
        corpus_name (str): The full resource name of the corpus to get information about.
                           Preferably use the resource_name from list_corpora results.
        tool_context (ToolContext): The tool context

    Returns:
        dict: Information about the corpus and its files
    """
    try:
        # Check if corpus exists
        if not check_corpus_exists(corpus_name, tool_context):
            return {
                "status": "error",
                "message": f"Corpus '{corpus_name}' does not exist",
                "corpus_name": corpus_name,
            }

        # Get the corpus resource name
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        # Try to get corpus details first
        corpus_display_name = corpus_name  # Default if we can't get actual display name

        # Process file information
        file_details = []
        try:
            # Get the list of files
            files = rag.list_files(corpus_resource_name)
            for rag_file in files:
                # Get document specific details
                try:
                    # Extract the file ID from the name
                    file_id = rag_file.name.split("/")[-1]

                    file_info = {
                        "file_id": file_id,
                        "display_name": (
                            rag_file.display_name
                            if hasattr(rag_file, "display_name")
                            else ""
                        ),
                        "source_uri": (
                            rag_file.source_uri
                            if hasattr(rag_file, "source_uri")
                            else ""
                        ),
                        "create_time": (
                            str(rag_file.create_time)
                            if hasattr(rag_file, "create_time")
                            else ""
                        ),
                        "update_time": (
                            str(rag_file.update_time)
                            if hasattr(rag_file, "update_time")
                            else ""
                        ),
                    }

                    file_details.append(file_info)
                except Exception:
                    # Continue to the next file
                    continue
        except Exception:
            # Continue without file details
            pass

        # Basic corpus info
        return {
            "status": "success",
            "message": f"Successfully retrieved information for corpus '{corpus_display_name}'",
            "corpus_name": corpus_name,
            "corpus_display_name": corpus_display_name,
            "file_count": len(file_details),
            "files": file_details,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error getting corpus information: {str(e)}",
            "corpus_name": corpus_name,
        }
        
def list_corpora() -> dict:
    """
    List all available Vertex AI RAG corpora.

    Returns:
        dict: A list of available corpora and status, with each corpus containing:
            - resource_name: The full resource name to use with other tools
            - display_name: The human-readable name of the corpus
            - create_time: When the corpus was created
            - update_time: When the corpus was last updated
    """
    try:
        # Get the list of corpora
        corpora = rag.list_corpora()

        # Process corpus information into a more usable format
        corpus_info: List[Dict[str, Union[str, int]]] = []
        for corpus in corpora:
            corpus_data: Dict[str, Union[str, int]] = {
                "resource_name": corpus.name,  # Full resource name for use with other tools
                "display_name": corpus.display_name,
                "create_time": (
                    str(corpus.create_time) if hasattr(corpus, "create_time") else ""
                ),
                "update_time": (
                    str(corpus.update_time) if hasattr(corpus, "update_time") else ""
                ),
            }

            corpus_info.append(corpus_data)

        return {
            "status": "success",
            "message": f"Found {len(corpus_info)} available corpora",
            "corpora": corpus_info,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error listing corpora: {str(e)}",
            "corpora": [],
        }
        
