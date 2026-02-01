"""
PDF report generation utilities.
"""
from io import BytesIO
from typing import Dict, List, Any


def _build_pdf(title: str, sections: List[Dict[str, Any]]) -> bytes:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
    except ImportError as exc:
        raise RuntimeError("reportlab is required for PDF reports") from exc

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    for section in sections:
        header = section.get("title")
        if header:
            story.append(Paragraph(header, styles["Heading2"]))
            story.append(Spacer(1, 6))

        content = section.get("content", {})
        if isinstance(content, dict):
            rows = [["Field", "Value"]]
            for key, value in content.items():
                rows.append([str(key), str(value)])
            table = Table(rows, hAlign="LEFT")
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 12))
        elif isinstance(content, list):
            for line in content:
                story.append(Paragraph(str(line), styles["BodyText"]))
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph(str(content), styles["BodyText"]))
            story.append(Spacer(1, 12))

    doc.build(story)
    return buffer.getvalue()


class ReportGenerator:
    @staticmethod
    def generate_diagnostic_report(results: Any) -> bytes:
        if isinstance(results, str):
            content = results.splitlines()
        elif isinstance(results, dict):
            content = results
        else:
            content = {"output": str(results)}
        sections = [{"title": "Diagnostics", "content": content}]
        return _build_pdf("DiagnOStiX Diagnostic Report", sections)

    @staticmethod
    def generate_fix_summary(fixes: List[Dict[str, Any]]) -> bytes:
        rows = [["Fix", "Result", "Message"]]
        for item in fixes:
            rows.append([
                item.get("fix_id") or item.get("fix_name") or "Unknown",
                item.get("result") or item.get("status") or "",
                item.get("message") or item.get("error_message") or "",
            ])
        sections = [{"title": "Fix Summary", "content": rows}]

        # Convert rows to a table-friendly dict
        table_content = {f"{row[0]}": f"{row[1]} - {row[2]}" for row in rows[1:]}
        return _build_pdf("DiagnOStiX Fix Summary", [{"title": "Fix Summary", "content": table_content}])

    @staticmethod
    def generate_system_health_report(metrics: Dict[str, Any]) -> bytes:
        sections = [{"title": "System Health", "content": metrics}]
        return _build_pdf("DiagnOStiX System Health Report", sections)
