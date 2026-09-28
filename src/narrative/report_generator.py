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
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155'),
            spaceAfter=4
        )
        bullet_style = ParagraphStyle(
            'BulletCustom',
            parent=body_style,
            leftIndent=12,
            bulletIndent=4,
            spaceAfter=3
        )
        subhead_style = ParagraphStyle(
            'SubheadCustom',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True
        )

        story = []

        # Top Header Bar
        banner_table = Table([[
            Paragraph("<b>DEAL INTELLIGENCE AGENT (DIA) — EXECUTIVE DOSSIER</b>", ParagraphStyle('BannerL', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph(f"<b>STAGE: {opportunity_data.get('stage', 'N/A').upper()}</b>", ParagraphStyle('BannerR', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, alignment=2))
        ]], colWidths=[380, 160])
        banner_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(banner_table)
        story.append(Spacer(1, 10))

        # Title
        story.append(Paragraph(f"Account Intelligence Dossier: {account_name}", title_style))
        story.append(Spacer(1, 6))

        # KPI Metric Cards Table
        win_prob_pct = int(analytics_summary.get('win_probability', 0.5) * 100)
        kpi_data = [
            [
                Paragraph("<b>Projected ARR</b><br/><font size='13' color='#1E40AF'><b>${:,.2f}</b></font>".format(opportunity_data.get('arr', 0)), ParagraphStyle('KPICell', fontName='Helvetica', fontSize=8, leading=12)),
                Paragraph(f"<b>Win Probability</b><br/><font size='13' color='#059669'><b>{win_prob_pct}%</b></font>", ParagraphStyle('KPICell2', fontName='Helvetica', fontSize=8, leading=12)),
                Paragraph(f"<b>Account Health</b><br/><font size='13' color='#0F172A'><b>{analytics_summary.get('health_status', 'Healthy')}</b></font>", ParagraphStyle('KPICell3', fontName='Helvetica', fontSize=8, leading=12)),
                Paragraph(f"<b>Primary Risk Vector</b><br/><font size='10' color='#DC2626'><b>{analytics_summary.get('top_risk', 'None')}</b></font>", ParagraphStyle('KPICell4', fontName='Helvetica', fontSize=8, leading=12))
            ]
        ]
        t_kpi = Table(kpi_data, colWidths=[135, 135, 135, 135])
        t_kpi.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        story.append(t_kpi)
        story.append(Spacer(1, 12))

        # Section 1: Strategic Intelligence & Narrative Breakdown
        story.append(Paragraph("1. Strategic Opportunity Diagnostics & Recalled Intelligence", h2_style))
        raw_narrative = analytics_summary.get("pitch_narrative", "")
        
        # Parse sections cleanly
        lines = [line.strip() for line in raw_narrative.split("\n") if line.strip() and not line.startswith("=")]
        for line in lines:
            if line.startswith("EXECUTIVE SUMMARY") or line.startswith("Target Opportunity") or line.startswith("Model Estimated"):
                continue
            elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("4. "):
                story.append(Spacer(1, 3))
                story.append(Paragraph(f"<b>{line}</b>", subhead_style))
            elif line.startswith("- ") or line.startswith("• "):
                clean_bullet = line.lstrip("-• ").strip()
                story.append(Paragraph(f"• {clean_bullet}", bullet_style))
            else:
                story.append(Paragraph(line, body_style))

        story.append(Spacer(1, 8))

        # Section 2: Prescriptive Next-Best-Actions (NBA)
        story.append(Paragraph("2. Prescriptive Next-Best-Actions (NBA)", h2_style))
        nbas = analytics_summary.get("next_best_actions", ["Schedule follow-up meeting."])
        for nba in nbas:
            story.append(Paragraph(f"✔ <b>Action:</b> {nba}", bullet_style))

        # Section 3: Automated Google Workspace & Neon DB Execution Staging
        story.append(Spacer(1, 8))
        story.append(Paragraph("3. Workspace MCP Staging & Relational Audit", h2_style))
        ws_audit = [
            [Paragraph("<b>Channel / MCP Tool</b>", subhead_style), Paragraph("<b>Staged Artifact / Audit Log</b>", subhead_style), Paragraph("<b>Safety Status</b>", subhead_style)],
            [Paragraph("<b>Gmail Draft</b>", body_style), Paragraph("RFC 2822 Staged Draft with Custom ROI Pitch", body_style), Paragraph("<font color='#059669'><b>Staged (Human-in-Loop)</b></font>", body_style)],
            [Paragraph("<b>Google Calendar</b>", body_style), Paragraph("Executive Alignment Call (Includes Google Meet Link)", body_style), Paragraph("<font color='#059669'><b>Scheduled</b></font>", body_style)],
            [Paragraph("<b>Neon PostgreSQL</b>", body_style), Paragraph("Relational State & Health Log Committed via SQLAlchemy", body_style), Paragraph("<font color='#059669'><b>Committed</b></font>", body_style)],
        ]
        t_ws = Table(ws_audit, colWidths=[120, 280, 140])
        t_ws.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_ws)

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
