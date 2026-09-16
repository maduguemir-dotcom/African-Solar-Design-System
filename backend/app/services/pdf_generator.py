from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime
from typing import Dict, Optional

class PDFReportGenerator:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self.setup_styles()
    
    def setup_styles(self):
        self.styles.add(ParagraphStyle(
            name="CustomTitle",
            parent=self.styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1a5f2a"),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name="SectionHeader",
            parent=self.styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#2c7a3f"),
            spaceBefore=20,
            spaceAfter=10
        ))
    
    def add_header(self, canvas: Canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(colors.HexColor("#1a5f2a"))
        canvas.drawString(1*inch, 10.5*inch, "Solar PV Designer Pro Africa")
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.black)
        canvas.drawString(1*inch, 10.3*inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        canvas.restoreState()
    
    def create_table(self, data: list) -> Table:
        table = Table(data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c7a3f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 11),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.beige])
        ]))
        return table
    
    def generate_design_report(self, project_name: str, customer_name: Optional[str],
                              location: Optional[str], design_data: Dict) -> str:
        doc = SimpleDocTemplate(
            self.output_path, pagesize=A4,
            rightMargin=1*inch, leftMargin=1*inch,
            topMargin=1*inch, bottomMargin=1*inch
        )
        
        elements = []
        elements.append(Paragraph("Solar PV Designer Pro Africa", self.styles["CustomTitle"]))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Professional Solar System Design Report", self.styles["Heading3"]))
        elements.append(Spacer(1, 0.5*inch))
        
        project_info = [
            ["Project Name:", project_name],
            ["Date:", datetime.now().strftime("%Y-%m-%d")],
            ["System Type:", design_data.get("system_type", "Hybrid").title()],
        ]
        if customer_name:
            project_info.insert(1, ["Customer:", customer_name])
        if location:
            project_info.insert(2, ["Location:", location])
        
        info_table = Table(project_info, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f0f0")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.5*inch))
        
        elements.append(Paragraph("Executive Summary", self.styles["SectionHeader"]))
        summary = f"""This report presents a complete solar photovoltaic system design for {project_name}.
        The proposed system includes a {design_data["pv_system"]["actual_pv_capacity_kw"]} kW PV array,
        {design_data["battery_system"]["battery_capacity_kwh"]} kWh battery storage, and a
        {design_data["inverter_system"]["inverter_capacity_kw"]} kW inverter system."""
        elements.append(Paragraph(summary, self.styles["Normal"]))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("PV System Specifications", self.styles["SectionHeader"]))
        pv = design_data["pv_system"]
        pv_table = [
            ["Parameter", "Value"],
            ["PV Capacity", f"{pv['pv_capacity_kw']} kW"],
            ["Actual Installed Capacity", f"{pv['actual_pv_capacity_kw']} kW"],
            ["Number of Panels", f"{pv['num_pv_panels']} units"],
            ["Panel Wattage", f"{pv['pv_panel_wattage']} W"],
            ["Daily Energy Production", f"{pv['daily_production_kwh']} kWh"],
        ]
        elements.append(self.create_table(pv_table))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Battery Energy Storage System", self.styles["SectionHeader"]))
        batt = design_data["battery_system"]
        batt_table = [
            ["Parameter", "Value"],
            ["Total Battery Capacity", f"{batt['battery_capacity_kwh']} kWh"],
            ["Usable Capacity", f"{batt['usable_capacity_kwh']} kWh"],
            ["Battery Voltage", f"{batt['battery_voltage']} V"],
            ["Autonomy Days", f"{batt['autonomy_days']} days"],
        ]
        elements.append(self.create_table(batt_table))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Financial Analysis", self.styles["SectionHeader"]))
        fin = design_data["financial_analysis"]
        fin_table = [
            ["Item", "Cost (USD)"],
            ["PV Panels", f"${fin['pv_panel_cost']:,.2f}"],
            ["Battery System", f"${fin['battery_cost']:,.2f}"],
            ["Inverter", f"${fin['inverter_cost']:,.2f}"],
            ["Installation", f"${fin['installation_cost']:,.2f}"],
            ["Total System Cost", f"${fin['total_system_cost']:,.2f}"],
        ]
        elements.append(self.create_table(fin_table))
        elements.append(Spacer(1, 0.3*inch))
        
        roi_text = f"""Monthly Savings: ${fin["monthly_savings"]:,.2f} | Annual Savings: ${fin["annual_savings"]:,.2f}
        Payback Period: {fin["payback_period_years"]} years | 25-Year ROI: {fin["roi_25_years_percentage"]}%"""
        elements.append(Paragraph(roi_text, self.styles["Normal"]))
        
        doc.build(elements, onFirstPage=self.add_header, onLaterPages=self.add_header)
        return self.output_path

def generate_solar_report(output_path: str, project_name: str, design_data: Dict,
                         customer_name: str = None, location: str = None) -> str:
    generator = PDFReportGenerator(output_path)
    return generator.generate_design_report(project_name, customer_name, location, design_data)
