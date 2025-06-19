from pathlib import Path
import pydicom

def process_dicom_sr(file_path: Path) -> dict:
    try:
        ds = pydicom.dcmread(file_path)

        if not hasattr(ds, "ContentSequence"):
            return {
                "type": "dicom-sr",
                "filename": file_path.name,
                "content": "This DICOM file does not contain structured report (ContentSequence not found)."
            }

        content = []

        def extract_sr(sequence):
            for item in sequence:
                name = item.ConceptNameCodeSequence[0].CodeMeaning if "ConceptNameCodeSequence" in item else "Unnamed"
                value = None
                if "TextValue" in item:
                    value = item.TextValue
                elif "NumericValue" in item:
                    value = str(item.NumericValue)
                elif "CodeValue" in item:
                    value = item.CodeValue

                line = f"{name}: {value}" if value else name
                content.append(line)

                if "ContentSequence" in item:
                    extract_sr(item.ContentSequence)

        extract_sr(ds.ContentSequence)

        return {
            "type": "dicom-sr",
            "filename": file_path.name,
            "content": content
        }

    except Exception as e:
        return {
            "type": "dicom-sr",
            "filename": file_path.name,
            "error": f"⚠️ Error processing DICOM SR: {str(e)}"
        }
