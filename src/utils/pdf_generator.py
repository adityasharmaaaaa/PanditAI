from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class PDFReportGenerator:
    def __init__(self, buffer):
        self.buffer = buffer
        self.doc = SimpleDocTemplate(
            self.buffer, 
            pagesize=A4,
            rightMargin=50, leftMargin=50, 
            topMargin=50, bottomMargin=50
        )
        self.styles = getSampleStyleSheet()
        
        # --- CUSTOM STYLES ---
        self.styles.add(ParagraphStyle(
            name='PanditTitle', 
            parent=self.styles['Title'], 
            fontSize=28, 
            textColor=colors.HexColor('#4B0082'), 
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader', 
            parent=self.styles['Heading2'], 
            fontSize=16, 
            textColor=colors.HexColor('#2c3e50'),
            borderPadding=(0, 0, 5, 0),
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            name='BodyTextCustom', 
            parent=self.styles['BodyText'], 
            fontSize=11, 
            leading=14, 
            spaceAfter=10,
            alignment=4 # Justify
        ))

    def create_report(self, user_name, data):
        elements = []
        
        # --- 1. TITLE PAGE ---
        elements.append(Paragraph("🕉️ PanditAI", self.styles['PanditTitle']))
        elements.append(Paragraph(f"Vedic Destiny Report for {user_name}", self.styles['Heading2']))
        elements.append(Spacer(1, 20))
        
        # Meta Info Table
        meta_data = [
            ["Ascendant:", data['meta'].get('ascendant_sign', 'Unknown')],
            ["Destiny Score:", f"{data['meta'].get('destiny_score', 0)}/100"],
            ["Generated On:", "Today"] # You can add datetime.now()
        ]
        t = Table(meta_data, colWidths=[150, 200], hAlign='LEFT')
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#4B0082')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 30))
        
        # --- 2. PLANETARY TABLE ---
        elements.append(Paragraph("🪐 Planetary Coordinates", self.styles['SectionHeader']))
        
        # Table Header
        table_data = [["Planet", "Sign", "House", "Degree", "Retro"]]
        
        zodiac = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        for p_name, p_data in data['planets'].items():
            if p_name == "Ascendant": continue
            sign = zodiac[p_data['sign_id']]
            deg = f"{int(p_data['degree'])}° {int((p_data['degree']%1)*60)}'"
            house = p_data.get('house_number', '-')
            retro = "Yes" if p_data.get('is_retrograde') else "-"
            table_data.append([p_name, sign, house, deg, retro])
            
        t_planets = Table(table_data, colWidths=[80, 80, 60, 80, 60])
        t_planets.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4B0082')), # Header Color
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.lightgrey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.white]) # Striped rows
        ]))
        elements.append(t_planets)
        elements.append(PageBreak())

        # --- 3. LIFE ANALYSIS (Formatted Text) ---
        elements.append(Paragraph("📜 Detailed Life Analysis", self.styles['PanditTitle']))
        
        if data.get('ai_reading'):
            raw_text = data['ai_reading']
            # Clean Markdown
            lines = raw_text.split('\n')
            for line in lines:
                line = line.strip()
                if not line: continue
                
                if line.startswith('###'):
                    # Section Header
                    header_text = line.replace('###', '').strip()
                    elements.append(Spacer(1, 10))
                    elements.append(Paragraph(header_text, self.styles['SectionHeader']))
                elif line.startswith('-') or line.startswith('*'):
                    # Bullet points
                    bullet_text = line.replace('-', '').replace('*', '').strip()
                    elements.append(Paragraph(f"• {bullet_text}", self.styles['BodyTextCustom'], bulletText='•'))
                else:
                    # Regular text
                    elements.append(Paragraph(line, self.styles['BodyTextCustom']))
        
        elements.append(PageBreak())
        
        # --- 4. DASHA TIMELINE ---
        elements.append(Paragraph("⏳ Vimshottari Dasha Timeline", self.styles['SectionHeader']))
        
        dasha_table = [["Mahadasha Lord", "Start Date", "End Date"]]
        if data.get('dasha') and data['dasha'].get('timeline'):
            for period in data['dasha']['timeline']:
                dasha_table.append([period['lord'], period['start'], period['end']])
                
        t_dasha = Table(dasha_table, colWidths=[150, 100, 100])
        t_dasha.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, colors.lightgrey),
        ]))
        elements.append(t_dasha)

        # Final Build
        self.doc.build(elements)