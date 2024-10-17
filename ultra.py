import re
import csv
import pypandoc

def rtf_to_text(rtf_file):
    text = pypandoc.convert_file(rtf_file, 'plain')
    return text

def parse_content(text):
    print("Converted Text:\n", text)  # Debug
    
    pattern = r'#(\d+)\s*\[\s*(.*?)\s*\]\s*\(\s*(.*?)\s*\)\s*(.*?)\s*--\s*(.*?)(?=\n#|\Z)'

    services = []

    matches = re.findall(pattern, text, re.DOTALL)
    
    print("Matches Found:\n", matches)  # Debug

    for match in matches:
        service_id = match[0].strip()  # Service ID
        service_title = match[1].strip()  # Service Title
        categories = match[2].strip()  # Categories
        description = match[3].strip()  # Description
        big_description = match[4].strip()  # Big Description
        
        services.append([service_id, service_title, categories, description, big_description])
    
    return services

def count_service_ids(text):
    return len(re.findall(r'#\d+', text))

def write_to_csv(services, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Service ID', 'Service Title', 'Categories', 'Description', 'Big Description'])
        writer.writerows(services)

def main(rtf_file, output_file):
    text = rtf_to_text(rtf_file)
    
    text = re.sub(r'\n+', '\n', text)  
    text = text.strip()  

    service_count = count_service_ids(text)
    print(f"Total number of service entries expected: {service_count}")

    services = parse_content(text)
    
    if services:
        write_to_csv(services, output_file)
        print(f"Converted {rtf_file} to {output_file} successfully!")
    else:
        print("No services found to write to CSV.")

if __name__ == "__main__":
    rtf_file = 'input.rtf'  # RTF file path
    output_file = 'output.csv'  # CSV Desired output
    main(rtf_file, output_file)
