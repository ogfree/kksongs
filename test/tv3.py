import os
import requests

def convert_url_to_markdown(url, include_title=True, ignore_links=False):
    api_url = "https://urltomarkdown.herokuapp.com"
    params = {
        'url': url,
        'title': str(include_title).lower(),
        'links': str(not ignore_links).lower()
    }

    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code} - {response.text}"

def convert_urls_to_md(url_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(url_file, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            markdown_content = convert_url_to_markdown(url)
            
            if "Error" not in markdown_content:
                # Extract title
                title_start = markdown_content.find("# ")
                title_end = markdown_content.find("\n", title_start)
                title = markdown_content[title_start + 2:title_end].strip()

                # Prepare front matter
                front_matter = f"+++\ntitle = \"{title}\"\ndate = \"2024-08-07\"\n+++\n\n"
                markdown_content = front_matter + markdown_content

                # Save markdown file
                output_file_name = f"{url.split('/')[-1].replace('.html', '')}.md"
                output_file_path = os.path.join(output_folder, output_file_name)
                with open(output_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_content)
                print(f"Converted '{url}' to '{output_file_name}'")
            else:
                print(f"Error converting '{url}': {markdown_content}")

url_file = 'urlsu.txt'
output_folder = '../content/posts/unicode'
convert_urls_to_md(url_file, output_folder)
