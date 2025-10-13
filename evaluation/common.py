from datetime import datetime
import json
import os
from pathlib import Path
import shutil
from typing import Any
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def convert_json_to_jsonl(filePath: str) -> str:
    """
    Convert the JSON file to JSONL format

    Args:
        filePath (str): path to the JSON file
    Returns:
        str: path to the JSONL file
    """

    print(f"Converting JSON to JSONL: {filePath}")

    outputPath = filePath.replace(".json", ".jsonl")
    with open(filePath, encoding="utf-8") as inputFile:
        with open(outputPath, "w", encoding="utf-8") as outputFile:
            json_data = json.load(inputFile)
            for entry in json_data:
                json.dump(entry, outputFile)
                outputFile.write("\n")

    return outputPath


def save_to_file(
    metrics: list[dict[str, Any]],
    detailed_results: list[dict[str, Any]],
    output_dir: str,
):
    """
    Save the evaluation results to a file
    Args:
        metrics (list[dict[str, Any]]): evaluation metrics
        detailed_results (list[dict[str, Any]]): detailed evaluation results
        output_dir (str): path to the output directory
    """

    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/evaluation_results.json", "w+") as f:
        f.write(json.dumps(detailed_results, ensure_ascii=False, indent=2))

    with open(f"{output_dir}/evaluation_metrics.json", "w+") as f:
        f.write(json.dumps(metrics, indent=2))


def generate_experiment_name(name: str = "Eval") -> str:
    """
    Generate a unique experiment name

    Args:
        description (str): description of the experiment

    Returns:
        str: unique experiment name
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    return f"{name}_{timestamp}"


def copy_and_execute_notebook(
    notebook_name: str, root_path: Path, output_path: Path
) -> None:
    """
    Copy and execute a notebook to the output directory

    Args:
        notebook_name (str): Name of the notebook file
        root_path (Path): Root path where the notebook is located
        output_path (Path): Path to the output directory where the notebook will be copied
    """
    notebook_src = root_path / notebook_name
    notebook_dst = output_path / notebook_name

    try:
        print(f"Copying notebook from {notebook_src} to {notebook_dst}")
        shutil.copy(notebook_src, notebook_dst)

        # Execute all cells in the notebook after copying
        with open(notebook_dst, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType] As required by nbformat

        ep = ExecutePreprocessor(kernel_name="python3")
        try:
            print(f"Executing notebook: {notebook_dst}")
            ep.preprocess(nb, {"metadata": {"path": os.path.dirname(notebook_dst)}})
            with open(notebook_dst, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType] As required by nbformat
            print(f"Executed and saved notebook with outputs: {notebook_dst}")
        except Exception as e:
            print(f"Failed to execute notebook: {e}")
    except Exception as e:
        print(f"Could not copy notebook: {e}")
