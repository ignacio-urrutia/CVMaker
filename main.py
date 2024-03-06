import json
import asyncio
from pyppeteer import launch


def json_to_html(json_file):
    contact_icons = {
        'phone': 'fa-solid fa-phone',
        'email': 'fa-solid fa-envelope',
        'website': 'fa-solid fa-globe',
        'linkedin': 'fa-brands fa-linkedin',
        'github': 'fa-brands fa-github',
        'twitter': 'fa-brands fa-twitter',
        'location': 'fa-solid fa-map-marker-alt',
        'default': 'fa-solid fa-circle-user'
    }


    with open(json_file, 'r') as file:
        cv_data = json.load(file)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{cv_data['personal_info']['name']}'s CV</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .section {{ margin-bottom: 20px; }}
            .cv-title {{ font-size: 50px; margin-bottom: 20px; font-weight: bold; text-transform: uppercase; }}
            .cv-subtitle {{ font-size: 24px; margin-bottom: 20px; font-weight: bold; }}
            .cv-header {{ margin-bottom: 40px; text-align: center; }}
            .section-title {{ font-size: 24px; margin-bottom: 10px; }}
            .contact-info {{ display: flex; flex-direction: row; justify-content: space-around; }}
            .item {{ margin-bottom: 5px; }}
            .details {{ margin-left: 20px; }}
            .details li {{ margin-bottom: 5px; }}
        </style>
        <script src="https://kit.fontawesome.com/265b36fe9b.js" crossorigin="anonymous"></script>
    </head>
    <body>
        <div class="cv-header">
            <p class="cv-title">{cv_data['personal_info']['name']}</p>
            <p class="cv-subtitle">{cv_data['personal_info']['title']}</p>
        </div>

        <div class="contact-info section">
            {''.join(f"<div class='item'><i class='fas {contact_icons.get(contact, contact_icons['default'])}'></i> {cv_data['contact_info'][contact]}</div>" for contact in cv_data['contact_info'])}
        </div>

        <div class="section">
            <div class="section-title">Summary</div>
            <p>{cv_data['summary']}</p>
        </div>

        <div class="section">
            <div class="section-title">Experience</div>
            {''.join(f"<div class='item'><b>{exp['position']}</b> at {exp['company']} ({exp['from']} - {exp['to']})<ul class='details'>{''.join(f"<li>{detail}</li>" for detail in exp['details'])}</ul></div>" for exp in cv_data['experience'])}
        </div>

        <div class="section">
            <div class="section-title">Education</div>
            {''.join(f"""
                     <div class='item'><b>{edu['degree']}</b>, {edu['institution']} ({edu['from']} - {edu['to']})</div>
                     """ for edu in cv_data['education'])}
        </div>

        <div class="section">
            <div class="section-title">Projects</div>
            {''.join(f"<div class='item'><b>{proj['name']}</b>: {proj['description']} - <a href='{proj['link']}'>Link</a> (Technologies: {', '.join(proj['technologies'])})</div>" for proj in cv_data['projects'])}
        </div>

        <div class="section">
            <div class="section-title">Skills</div>
            <ul class="details">
                {''.join(f"<li>{skill}</li>" for skill in cv_data['skills'])}
            </ul>
        </div>

        <div class="section">
            <div class="section-title">Certifications</div>
            {''.join(f"<div class='item'>{cert['name']} (Issuer: {cert['issuer']}, Date: {cert['date']})</div>" for cert in cv_data['certifications'])}
        </div>

    </body>
    </html>
    """
    
    output_filename = json_file.replace('.json', '.html')
    with open(output_filename, 'w') as output_file:
        output_file.write(html_content)

    print(f"HTML CV generated successfully: {output_filename}")

async def generate_pdf_from_html(html_content, pdf_path):
    browser = await launch(headless= True,
                           defaultViewport= None,
                           executablePath= '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    page = await browser.newPage()
    
    await page.setContent(html_content)

    # Sleep for 5 seconds to allow the PDF to be generated
    await asyncio.sleep(1)

    # await page.goto('https://www.nachourrutia.com')
    
    await page.screenshot({'path': 'example.png', 'fullPage': True})

    await page.pdf({'path': pdf_path, 'format': 'A4'})

    
    await browser.close()


# Replace 'your_cv.json' with the path to your JSON file
json_to_html('cv.json')


html_content = open('cv.html', 'r').read()
pdf_path = 'cv.pdf'
asyncio.get_event_loop().run_until_complete(generate_pdf_from_html(html_content, pdf_path))