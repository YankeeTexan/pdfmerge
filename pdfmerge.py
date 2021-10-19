import argparse
import os

from PyPDF2 import PdfFileMerger

PARSER = argparse.ArgumentParser()
# Add an argument for the PDF files
PARSER.add_argument('pdfs', nargs='+',
                    help='The pdfs to merge or the directory containing the pdfs.')
# Add an argument for the output file name
PARSER.add_argument("-o", "--output",
                    help="Set the output file name.",
                    metavar="OUTPUT")
# Collect the arguments
args = PARSER.parse_args()

if len(args.pdfs) == 0:
    raise RuntimeError("No PDF files provided. Exiting.")

if args.output is None:
    raise RuntimeError("No output file name provided.")
elif args.output.find("pdf") < 0:
    args.output = args.output + ".pdf"

MERGER = PdfFileMerger()
try:
    # Add the pdfs to the merged file unless they are not PDFs.
    if len(args.pdfs) == 1:
        for filename in os.listdir(args.pdfs[0]):
            if filename.endswith(".pdf"):
                print(f"Appending {os.path.join(args.pdfs[0], filename)}")
                MERGER.append(os.path.join(args.pdfs[0], filename))
    else:
        for pdf in args.pdfs:
            if os.path.splitext(pdf)[1] == ".pdf":
                print(f"Appending {pdf}")
                MERGER.append(os.path.join(os.getcwd(), pdf))
            else:
                print(f"File {pdf} is not a pdf. Skipping.")

    # Write output file
    MERGER.write(args.output)
except Exception as e:
    print(e)
finally:
    MERGER.close()
