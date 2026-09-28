import os
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class ReportGenerator:
    """
    Generates Deal Dossier reports and exports high-resolution PDF dossiers
    and Google Docs structured export representations.
    """
    def generate_pdf_dossier(
        self,
        output_filepath: str,
        account_name: str,
        opportunity_data: Dict[str, Any],
        analytics_summary: Dict[str, Any]
    ) -> str:
        """
        Builds a programmatic PDF Deal Dossier using ReportLab.
        """
        doc = SimpleDocTemplate(
            output_filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=12
        )
        h2_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2b6cb0'),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodyTextCustom',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#2d3748')
        )

        story = []

        # Header Title
        story.append(Paragraph(f"DEAL DOSSIER & INTELLIGENCE REPORT: {account_name}", title_style))
        story.append(Spacer(1, 10))

        # Snapshot Table
        snapshot_data = [
            ["Account Name", account_name, "Deal Stage", opportunity_data.get("stage", "N/A")],
            ["Projected ARR", f"${opportunity_data.get('arr', 0):,.2f}", "Win Probability", f"{int(analytics_summary.get('win_probability', 0.5) * 100)}%"],
            ["Health Status", analytics_summary.get("health_status", "Healthy"), "Top Risk Vector", analytics_summary.get("top_risk", "None")]
        ]
        t = Table(snapshot_data, colWidths=[110, 150, 110, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))

        # Section 1: Executive Summary
        story.append(Paragraph("1. Executive Snapshot & Win-Loss Diagnostics", h2_style))
        story.append(Paragraph(analytics_summary.get("pitch_narrative", "Executive summary pending..."), body_style))
        story.append(Spacer(1, 10))

        # Section 2: Prescriptive Next Steps
        story.append(Paragraph("2. Prescriptive Next-Best-Actions (NBA)", h2_style))
        nbas = analytics_summary.get("next_best_actions", ["Schedule follow-up meeting."])
        for nba in nbas:
            story.append(Paragraph(f"• {nba}", body_style))

        doc.build(story)
        return output_filepath

    def generate_google_doc_export(
        self,
        account_name: str,
        opportunity_data: Dict[str, Any],
        analytics_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates structured JSON schema for Google Docs docs.documents.create and batchUpdate.
        """
        return {
            "title": f"Deal Dossier - {account_name}",
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": f"DEAL DOSSIER: {account_name}\nStage: {opportunity_data.get('stage')}\nARR: ${opportunity_data.get('arr')}\n\nSummary:\n{analytics_summary.get('pitch_narrative')}\n"
                    }
                }
            ]
        }
