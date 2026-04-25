from weasyprint import HTML
import base64

def generate_pdf(data):
   
    UserName = data["full_name"]
    UserEmail = data["email"]
    BookName = data["title"]
    borrowed_date = data["borrow_date"]
    return_date = data["return_date"]

    
    stamp_svg = """
    <svg width="100" height="100" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="45" stroke="#e74c3c" stroke-width="5" fill="none" />
    <text x="50" y="55" font-family="Arial" font-size="16" fill="#e74c3c" 
            text-anchor="middle" font-weight="bold" transform="rotate(-15 50 50)">APPROVED</text>
    </svg>
    """
    stamp_b64 = base64.b64encode(stamp_svg.encode('utf-8')).decode('utf-8')

    html_template = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 20mm; }}
            body {{ font-family: 'Helvetica', sans-serif; color: #333; }}
            .slip-container {{ 
                border: 2px solid #2c3e50; 
                padding: 40px; 
                border-radius: 10px; 
                position: relative;
            }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #2c3e50; }}
            .details {{ margin: 30px 0; }}
            .row {{ margin-bottom: 15px; }}
            .label {{ font-weight: bold; color: #555; width: 150px; display: inline-block; }}
            .footer {{ margin-top: 50px; border-top: 1px solid #ddd; padding-top: 20px; font-size: 0.9em; }}
            .stamp {{ position: absolute; top: 20px; right: 20px; width: 100px; }}
        </style>
    </head>
    <body>
        <div class="slip-container">
            <img src="data:image/svg+xml;base64,{stamp_b64}" class="stamp" alt="Stamp">
            <h1>Library Borrowing Record</h1>
            <p>Official borrowing slip for library circulation.</p>
            
            <div class="details">
                <div class="row"><span class="label">Borrower:</span> {UserName}</div>
                <div class="row"><span class="label">Book Title:</span> {BookName}</div>
                <div class="row"><span class="label">Date Borrowed:</span> {borrowed_date}</div>
                <div class="row"><span class="label">Due Date:</span> {return_date}</div>
            </div>
            
            <div class="footer">
                <p><strong>Policy:</strong> Please return this book to the circulation desk by the due date.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Generate and return the PDF bytes
    return HTML(string=html_template).write_pdf()

        

    
    



