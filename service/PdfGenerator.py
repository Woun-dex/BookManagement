from weasyprint import HTML
import base64
from datetime import datetime

def generate_pdf(data):
   
    LibrarianName = data.get("full_name", "N/A")
    LibrarianEmail = data.get("email", "N/A")
    BookName = data.get("title", "N/A")
    borrowed_date = data.get("borrow_date", "N/A")
    return_date = data.get("return_date", "N/A")
    ReaderId = data.get("reader_id", "N/A")
    ReaderName = data.get("reader_name", "N/A")
    ReaderEmail = data.get("reader_email", "N/A")
    
    # Format dates cleanly
    def fmt_date(d):
        try:
            dt = datetime.fromisoformat(str(d).replace(" ", "T").split(".")[0])
            return dt.strftime("%B %d, %Y")
        except:
            return str(d)
    
    borrowed_fmt = fmt_date(borrowed_date)
    return_fmt = fmt_date(return_date)
    today_fmt = datetime.now().strftime("%B %d, %Y")
    receipt_no = f"RCT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    stamp_svg = """
    <svg width="120" height="120" viewBox="0 0 120 120">
    <circle cx="60" cy="60" r="52" stroke="#16a34a" stroke-width="4" fill="none" opacity="0.8"/>
    <circle cx="60" cy="60" r="44" stroke="#16a34a" stroke-width="1.5" fill="none" opacity="0.5"/>
    <text x="60" y="56" font-family="Arial" font-size="14" fill="#16a34a" 
            text-anchor="middle" font-weight="bold" transform="rotate(-12 60 60)">APPROVED</text>
    <text x="60" y="74" font-family="Arial" font-size="8" fill="#16a34a" 
            text-anchor="middle" opacity="0.7">LIBRARY SYSTEM</text>
    </svg>
    """
    stamp_b64 = base64.b64encode(stamp_svg.encode('utf-8')).decode('utf-8')

    html_template = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 0; }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif; 
                color: #1e293b;
                background: #f8fafc;
            }}
            
            .page {{
                width: 210mm;
                min-height: 297mm;
                padding: 0;
                position: relative;
            }}
            
            /* Header Band */
            .header {{
                background: linear-gradient(135deg, #ea580c, #c2410c);
                color: white;
                padding: 40px 50px;
                position: relative;
                overflow: hidden;
            }}
            .header::after {{
                content: "";
                position: absolute;
                top: -50px;
                right: -50px;
                width: 200px;
                height: 200px;
                background: rgba(255,255,255,0.08);
                border-radius: 50%;
            }}
            .header h1 {{
                font-size: 28px;
                font-weight: 800;
                letter-spacing: -0.5px;
                margin-bottom: 4px;
            }}
            .header .subtitle {{
                font-size: 13px;
                opacity: 0.85;
                font-weight: 400;
            }}
            .header .receipt-no {{
                position: absolute;
                top: 40px;
                right: 50px;
                text-align: right;
            }}
            .header .receipt-no .label {{
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 2px;
                opacity: 0.7;
            }}
            .header .receipt-no .value {{
                font-size: 14px;
                font-weight: 700;
                margin-top: 2px;
            }}
            
            /* Content */
            .content {{
                padding: 40px 50px;
            }}
            
            /* Info Grid */
            .info-grid {{
                display: flex;
                gap: 30px;
                margin-bottom: 40px;
            }}
            .info-card {{
                flex: 1;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 24px;
                position: relative;
            }}
            .info-card .card-label {{
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 2px;
                color: #94a3b8;
                font-weight: 700;
                margin-bottom: 16px;
            }}
            .info-card .field {{
                margin-bottom: 12px;
            }}
            .info-card .field .field-label {{
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: #94a3b8;
                font-weight: 600;
                margin-bottom: 3px;
            }}
            .info-card .field .field-value {{
                font-size: 15px;
                color: #1e293b;
                font-weight: 600;
            }}
            
            /* Book Section */
            .book-section {{
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 28px;
                margin-bottom: 30px;
                position: relative;
            }}
            .book-section .section-title {{
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 2px;
                color: #94a3b8;
                font-weight: 700;
                margin-bottom: 12px;
            }}
            .book-name {{
                font-size: 24px;
                font-weight: 800;
                color: #0f172a;
                letter-spacing: -0.3px;
            }}
            
            /* Date Strip */
            .date-strip {{
                display: flex;
                gap: 0;
                margin-bottom: 30px;
                border-radius: 12px;
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }}
            .date-item {{
                flex: 1;
                padding: 20px 24px;
                background: white;
            }}
            .date-item:first-child {{
                border-right: 1px solid #e2e8f0;
            }}
            .date-item .date-label {{
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 2px;
                color: #94a3b8;
                font-weight: 700;
                margin-bottom: 6px;
            }}
            .date-item .date-value {{
                font-size: 18px;
                font-weight: 700;
                color: #0f172a;
            }}
            .date-item.due .date-value {{
                color: #ea580c;
            }}
            
            /* Stamp */
            .stamp {{
                position: absolute;
                top: 10px;
                right: 20px;
                width: 100px;
                opacity: 0.9;
                transform: rotate(8deg);
            }}
            
            /* Policy */
            .policy {{
                background: #fffbeb;
                border: 1px solid #fef3c7;
                border-radius: 10px;
                padding: 20px 24px;
                margin-bottom: 40px;
            }}
            .policy .policy-title {{
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: #92400e;
                margin-bottom: 8px;
            }}
            .policy p {{
                font-size: 12px;
                color: #78716c;
                line-height: 1.6;
            }}
            
            /* Signature */
            .signature-row {{
                display: flex;
                gap: 40px;
                margin-top: 50px;
                padding-top: 30px;
            }}
            .sig-box {{
                flex: 1;
                text-align: center;
            }}
            .sig-line {{
                border-top: 2px solid #cbd5e1;
                padding-top: 10px;
                margin-top: 50px;
            }}
            .sig-label {{
                font-size: 11px;
                color: #64748b;
                font-weight: 600;
            }}
            .sig-name {{
                font-size: 12px;
                color: #94a3b8;
                margin-top: 2px;
            }}
            
            /* Footer */
            .footer {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 16px 50px;
                background: #f1f5f9;
                border-top: 1px solid #e2e8f0;
                display: flex;
                justify-content: space-between;
                font-size: 10px;
                color: #94a3b8;
            }}
        </style>
    </head>
    <body>
        <div class="page">
            <!-- Header -->
            <div class="header">
                <h1>📚 Books Library</h1>
                <div class="subtitle">Official Borrowing Receipt</div>
                <div class="receipt-no">
                    <div class="label">Receipt No.</div>
                    <div class="value">{receipt_no}</div>
                </div>
            </div>
            
            <div class="content">
                <!-- Reader & Librarian Info -->
                <div class="info-grid">
                    <div class="info-card">
                        <div class="card-label">Reader Information</div>
                        <div class="field">
                            <div class="field-label">Full Name</div>
                            <div class="field-value">{ReaderName}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">Email</div>
                            <div class="field-value">{ReaderEmail}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">Reader ID</div>
                            <div class="field-value">#{ReaderId}</div>
                        </div>
                    </div>
                    <div class="info-card">
                        <div class="card-label">Issued By</div>
                        <div class="field">
                            <div class="field-label">Librarian</div>
                            <div class="field-value">{LibrarianName}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">Email</div>
                            <div class="field-value">{LibrarianEmail}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">Date Issued</div>
                            <div class="field-value">{today_fmt}</div>
                        </div>
                    </div>
                </div>
                
                <!-- Book -->
                <div class="book-section">
                    <img src="data:image/svg+xml;base64,{stamp_b64}" class="stamp" alt="Stamp">
                    <div class="section-title">Book Details</div>
                    <div class="book-name">{BookName}</div>
                </div>
                
                <!-- Dates -->
                <div class="date-strip">
                    <div class="date-item">
                        <div class="date-label">Date Borrowed</div>
                        <div class="date-value">{borrowed_fmt}</div>
                    </div>
                    <div class="date-item due">
                        <div class="date-label">Return By</div>
                        <div class="date-value">{return_fmt}</div>
                    </div>
                </div>
                
                <!-- Policy -->
                <div class="policy">
                    <div class="policy-title">📋 Library Policy</div>
                    <p>Please return this book by the due date. Late returns may incur a fee of $0.50 per day. 
                    Books must be returned in the same condition as borrowed. Damaged or lost books will require replacement at full retail value.</p>
                </div>
                
                <!-- Signatures -->
                <div class="signature-row">
                    <div class="sig-box">
                        <div class="sig-line">
                            <div class="sig-label">Librarian Signature</div>
                            <div class="sig-name">{LibrarianName}</div>
                        </div>
                    </div>
                    <div class="sig-box">
                        <div class="sig-line">
                            <div class="sig-label">Reader Signature</div>
                            <div class="sig-name">{ReaderName}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <span>Books Library Management System</span>
                <span>Generated on {today_fmt}</span>
            </div>
        </div>
    </body>
    </html>
    """

    return HTML(string=html_template).write_pdf()
