from lxml import etree
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def xml_to_pdf(xml_file, pdf_filename):
    # Parse XML
    tree = etree.parse(xml_file)
    root = tree.getroot()
    
    # Define PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], spaceAfter=10)
    body_style = styles["BodyText"]
    
    # Add title
    elements.append(Paragraph(f"XML Document: {root.tag}", title_style))
    elements.append(Spacer(1, 12))

    # Function to format XML content
    def process_element(element, indent=0):
        nonlocal elements
        
        # Add element name as heading
        elements.append(Paragraph(f"{'&nbsp;' * indent * 4} ➤ <b>{element.tag}</b>", heading_style))
        
        # If element has text, add it
        if element.text and element.text.strip():
            elements.append(Paragraph(f"{'&nbsp;' * (indent + 1) * 4} {element.text.strip()}", body_style))
        
        # If element has attributes, show in a table
        if element.attrib:
            table_data = [["Attribute", "Value"]] + [[k, v] for k, v in element.attrib.items()]
            table = Table(table_data, colWidths=[100, 300])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 8))

        # Process child elements recursively
        for child in element:
            process_element(child, indent + 1)

    process_element(root)
    
    # Build PDF
    doc.build(elements)
    print(f"PDF saved as: {pdf_filename}")

# Usage Example
xml_to_pdf("response_files/response.xml", "response_files/output.pdf")
