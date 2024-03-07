import json
import asyncio
import sys
from pyppeteer import launch
from secrets import token_urlsafe
import os

TEMP_PATH = os.path.join(os.path.dirname(__file__), 'temp')

def json_to_html(json_file, language='english', output_filename='cv.html'):
    titles = {
        'english': {
            'summary': 'Summary',
            'experience': 'Experience',
            'education': 'Education',
            'projects': 'Projects',
            'skills': 'Skills',
            'certifications': 'Certifications',
            'extra_experience': 'Other Experience',
            'languages': 'Languages',
            'more_info': 'More About Me',
            'interests': 'Other Interests',
            'references': 'References'
        },
        'spanish': {
            'summary': 'Resumen',
            'experience': 'Experiencia',
            'education': 'Educación',
            'projects': 'Proyectos',
            'skills': 'Habilidades',
            'certifications': 'Certificaciones',
            'extra_experience': 'Otras Experiencias',
            'languages': 'Idiomas',
            'more_info': 'Más Sobre Mí',
            'interests': 'Otros Intereses',
            'references': 'Referencias'
        }
    }

    titles_dict = titles.get(language, titles['english'])

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

    contant_links = {
        'phone': 'tel:',
        'email': 'mailto:',
        'website': 'https://www.',
        'linkedin': 'https://www.linkedin.com/in/',
        'github': 'https://www.github.com/',
        'twitter': 'https://www.twitter.com/',
        'location': '',
        'default': ''
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
            .cv-title {{ font-size: 50px; margin-bottom: 20px; font-weight: bolder; text-transform: uppercase; }}
            .cv-subtitle {{ font-size: 24px; margin-bottom: 20px; font-weight: bold; }}
            .cv-header {{ margin-bottom: 40px; text-align: center; }}
            .section-title {{ font-size: 24px; margin-bottom: 10px; font-weight: bold; text-transform: uppercase; }}
            
            .summary-section {{ text-align: justify; }}

            .contact-info {{ display: flex; flex-direction: row; justify-content: center; flex-wrap: wrap; }}
            .contact-info .item {{ margin-left: 20px; margin-right: 20px; margin-bottom: 10px; }}
            
            .experience_item_header {{ display: flex; justify-content: space-between; }}
            .experience_company {{ font-size: 20px; font-weight: bold; }}
            .experience_position {{ font-size: 18px; }}

            .item {{ margin-bottom: 5px; }}
            .details {{ margin-left: 20px; }}
            .details li {{ margin-bottom: 5px; }}

            .progress {{ height: 10px; background-color: #d1d1d1; width: 150px; border-radius: 5px; }}
            .progress-bar {{ background-color: #3C409F; height: 10px; border-radius: 5px; }}
            
            .languages-section {{ display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-around; }}

            .skills-list {{ display: flex; list-style: none;  flex-direction: row; flex-wrap: wrap; padding: 0; }}
            .skills-list li {{ margin-right: 20px; margin-bottom: 20px; }}

            .custom_space {{ padding-bottom: 120px; }}

            ul {{ padding: 0; }}


            @media print {{
                body {{-webkit-print-color-adjust: exact;}}
            }}
        </style>
        <script src="https://kit.fontawesome.com/265b36fe9b.js" crossorigin="anonymous"></script>
    </head>
    <body>
        <div class="cv-header">
            <p class="cv-title">{cv_data['personal_info']['name']}</p>
            <p class="cv-subtitle">{cv_data['personal_info']['title']}</p>
        </div>

        <div class="contact-info section">
            {''.join(f"""
                     <div class='item'>
                        <i class='fas {contact_icons.get(contact, contact_icons['default'])}'></i>
                        <a href='{contant_links.get(contact, '')}{cv_data['contact_info'][contact]}'>{cv_data['contact_info'][contact]}</a>
                    </div>
                     """ for contact in cv_data['contact_info'])}
        </div>

        <div class="section">
            <div class="section-title">{titles_dict['summary']}</div>
            <hr>
            <div class="summary-section">{cv_data['summary']}</div>
        </div>

        <div class="section">
            <div class="section-title">{titles_dict['experience']}</div>
            <hr>
            {''.join(f"""
                     <div class='item'>
                        <div class='experience_item_header'>
                            <div>
                                <div class='experience_company'>{exp['company']}</div> 
                                <div class='experience_position'>{exp['position']}</div>
                            </div>
                            <div class='experience_dates'>{exp['from']} - {exp['to']}</div>
                        </div>
                        <ul class='details'>{''.join(f"<li>{detail}</li>" for detail in exp['details'])}</ul></div>
                     """ for exp in cv_data['experience'])}
        </div>

        <div class="section">
            <div class="section-title">{titles_dict['education']}</div>
            <hr>
            {''.join(f"""
                     <div class='item'>
                        <b>{edu['institution']}</b>: {edu['degree']} ({edu['from']} - {edu['to']})</div>
                     """ for edu in cv_data['education'])}
        </div>

        {'' if 'projects' not in cv_data else f'''
        <div class="section">
            <div class="section-title">{titles_dict['projects']}</div>
            <hr>
            {''.join(f"<div class='item'><b>{proj['name']}</b>: {proj['description']} - <a href='{proj['link']}'>Link</a> (Technologies: {', '.join(proj['technologies'])})</div>" for proj in cv_data['projects'])}
        </div>
        '''}

        <div class="custom_space"></div>

        {'' if 'skills' not in cv_data else f'''
        <div class="section">
            <div class="section-title">{titles_dict['skills']}</div>
            <hr>
            <ul class="skills-list">
                {''.join(f"""
                            <li>{skill}
                                <div class="progress">
                                    <div class="progress-bar" role="progressbar" style="width: {value}%" aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                            </li>
                         """ for skill, value in cv_data['skills'].items() if value)}
            </ul>
        </div>
        '''}


        {'' if 'certifications' not in cv_data else f'''
        <div class="section">
            <div class="section-title">{titles_dict['certifications']}</div>
            <hr>
            {''.join(f"<div class='item'>{cert['name']} (Issuer: {cert['issuer']}, Date: {cert['date']})</div>" for cert in cv_data['certifications'])}
        </div>
        '''}


        {'' if 'extra_experience' not in cv_data else f'''
        <div class="section">
            <div class="section-title">{titles_dict['extra_experience']}</div>
            <hr>
            {''.join(f"<div class='item'><b>{exp['company']}</b> - {exp['description']} ({exp['from']} - {exp['to']})</div>" for exp in cv_data['extra_experience'])}
        </div>
        '''}

        {'' if 'languages' not in cv_data else f'''
        <div class="section">
            <div class="section-title">{titles_dict['languages']}</div>
            <hr>
            <div class="languages-section">
                {''.join(f"<div class='item'>{lang['name']} ({lang['level']})</div>" for lang in cv_data['languages'])}
            </div>
        </div>
        '''}


        {'' if 'more_info' not in cv_data else f'''
        <div class="section">
            <div class="section-title">{titles_dict['more_info']}</div>
            <hr>
            <p>{cv_data['more_info']}</p>
        </div>
        '''}

        {'' if 'interests' not in cv_data else f'''
        <div class="section">
            <div class="section-title">{titles_dict['interests']}</div>
            <div class="languages-section">
                {''.join(f"<div class='item'>{interest}</div>" for interest in cv_data['interests'])}
            </div>
        </div>
        '''}

    </body>
    </html>
    """

    with open(output_filename, 'w') as output_file:
        output_file.write(html_content)

    print(f"HTML CV generated successfully: {output_filename}")

async def generate_pdf_from_html(html_content, pdf_path):
    browser = await launch(headless= True,
                           defaultViewport= None,
                           executablePath= '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    page = await browser.newPage()
    
    await page.setContent(html_content)

    # Sleep for 1 seconds to allow the PDF to be generated
    await asyncio.sleep(1)
    
    await page.screenshot({'path': 'example.png', 'fullPage': True})

    await page.pdf({'path': pdf_path, 'format': 'A4'})

    
    await browser.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py <path-to-cv-json> <path-to-output-html> <language>')
        sys.exit(1)
    
    if len(sys.argv) == 4:
        json_path = sys.argv[1]
        output_path = sys.argv[2]
        language = sys.argv[3]
    elif len(sys.argv) == 3:
        json_path = sys.argv[1]
        output_path = sys.argv[2]
        language = 'english'
    elif len(sys.argv) == 2:
        json_path = sys.argv[1]
        output_path = 'cv.pdf'
        language = 'english'

    random_filename = os.path.join(TEMP_PATH, f'{token_urlsafe(8)}.html')
    json_to_html(json_path, language, random_filename)
    html_content = open(random_filename, 'r').read()

    asyncio.get_event_loop().run_until_complete(generate_pdf_from_html(html_content, output_path))