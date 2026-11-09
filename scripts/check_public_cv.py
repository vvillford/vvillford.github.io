"""Fail closed if the public CV contains private contact information."""
import pathlib
import re
import shutil
import subprocess
import sys


def extract(path):
    if shutil.which("pdftotext"):
        result = subprocess.run(
            ["pdftotext", str(path), "-"], check=True, capture_output=True, text=True
        )
        return result.stdout
    if sys.platform == "darwin" and shutil.which("swift"):
        code = '''import Foundation
import PDFKit
let pdf = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
print(pdf.string ?? "")
print(pdf.documentAttributes ?? [:])
for i in 0..<pdf.pageCount {
    for annotation in pdf.page(at: i)!.annotations {
        print(annotation.contents ?? "")
        print(annotation.url?.absoluteString ?? "")
    }
}
'''
        result = subprocess.run(
            ["swift", "-module-cache-path", "/private/tmp/public-cv-swift-cache",
             "-", str(path)], input=code, check=True, capture_output=True, text=True
        )
        return result.stdout
    raise RuntimeError("Install Poppler (pdftotext) to verify the public CV")


def main():
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "assets/cv.pdf")
    try:
        text = extract(path)
        if "WILLIAM FORD" not in text.upper() or len(text.strip()) < 500:
            raise RuntimeError("CV text extraction was incomplete")
        if re.search(r"cachan|tel:|phone|telephone", text, re.IGNORECASE):
            raise RuntimeError("Private location or phone contact found")
        if re.search(r"(?:\+\s*\d|00\d)[\d\s().-]{7,}\d", text):
            raise RuntimeError("Phone number found")
        if "M2 Optimisation, Games and Control" not in text:
            raise RuntimeError("Expected full course name missing")
    except Exception as error:
        print(f"Public CV privacy check FAILED: {error}", file=sys.stderr)
        return 1
    print("Public CV privacy check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
