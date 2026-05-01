import re

# Mapping user tags to system entity types or pattern keys
TAG_MAPPINGS = {
    # Person / Name related
    "name": "PERSON",
    "candidate name": "PERSON",
    "full name": "PERSON",
    "applicant": "PERSON",
    
    # Contact related
    "email": "PATTERN:email",
    "mail": "PATTERN:email",
    "mail id": "PATTERN:email",
    "email id": "PATTERN:email",
    "phone": "PATTERN:phone",
    "mobile": "PATTERN:phone",
    "contact": "PATTERN:phone",
    "cell": "PATTERN:phone",
    "number": "PATTERN:phone",
    
    # Web related
    "linkedin": "PATTERN:url",
    "github": "PATTERN:url",
    "portfolio": "PATTERN:url",
    "website": "PATTERN:url",
    "link": "PATTERN:url",
    "links": "PATTERN:url",
    
    # Date related
    "dob": "KEY_VALUE:dob",
    "date of birth": "KEY_VALUE:dob",
    "birth date": "KEY_VALUE:dob",
    "date": "PATTERN:date",
    
    # ID / Key-Value related
    "id": "KEY_VALUE:id",
    "roll no": "KEY_VALUE:id",
    "roll number": "KEY_VALUE:id",
    "enrollment no": "KEY_VALUE:id",
    "reg no": "KEY_VALUE:id",
    
    # Organization/Education (NER based)
    "company": "ORG",
    "organization": "ORG",
    "work": "ORG",
    "university": "ORG", # SpaCy often labels universities as ORG
    "college": "ORG",
    "school": "ORG", 
    "education": "KEYWORD:education", # Changed to KEYWORD for better context extraction
    
    # Location
    "location": "GPE",
    "city": "GPE",
    "country": "GPE",
    "address": "GPE",
    
    # Skills - Special Handling
    "skills": "KEYWORD:skills",
    "tech stack": "KEYWORD:skills",
    "technologies": "KEYWORD:skills",

    # Additional sections (Context-Based Extraction)
    "projects": "KEYWORD:projects",
    "project": "KEYWORD:projects",
    
    "certificates": "KEYWORD:certifications",
    "certifications": "KEYWORD:certifications",
    
    "experience": "KEYWORD:experience",
    "work experience": "KEYWORD:experience",
    "employment": "KEYWORD:experience",
    
    "summary": "KEYWORD:summary",
    "profile": "KEYWORD:summary",
    "objective": "KEYWORD:summary",
    "about": "KEYWORD:summary",
    
    "education": "KEYWORD:education", # Override previous ORG mapping to get full section
    "qualifications": "KEYWORD:education",
    
    "languages": "KEYWORD:languages",
    "known languages": "KEYWORD:languages",
    
    "achievements": "KEYWORD:achievements",
    "awards": "KEYWORD:achievements",
    
    "hobbies": "KEYWORD:hobbies",
    "interests": "KEYWORD:hobbies",
    
    "references": "KEYWORD:references",
    
    # Invoice / Key-Value related
    "invoice number": "KEY_VALUE:invoice_number",
    "invoice no": "KEY_VALUE:invoice_number",
    "bill no": "KEY_VALUE:invoice_number",
    
    "total amount": "KEY_VALUE:amount",
    "grand total": "KEY_VALUE:amount",
    "net amount": "KEY_VALUE:amount",
    
    "gst": "KEY_VALUE:gst",
    "gst no": "KEY_VALUE:gst",
    "gstin": "KEY_VALUE:gst",
    
    "state": "KEY_VALUE:state",
    "state name": "KEY_VALUE:state",
    "state code": "KEY_VALUE:state_code",
}

# Blocklist for Names (Common false positives)
NAME_BLOCKLIST = {
    # Tech stack & programming
    "java", "python", "c++", "c", "html", "css", "sql", "react", "node", "javascript", "js",
    "english", "hindi", "tamil", "german", "french", "spanish",
    "pandas", "numpy", "matplotlib", "scikit", "sklearn", "keras", "tensorflow", "pytorch",
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "github", "gitlab",
    "linux", "windows", "macos", "android", "ios", "flutter", "dart",
    
    # Document terms
    "resume", "curriculum", "vitae", "cv", "profile", "summary", "objective",
    "declaration", "education", "experience", "projects", "skills", "achievements",
    "certifications", "interests", "hobbies", "languages", "references", "contacts",
    "work", "employment", "history", "date", "birth", "dob", "gender", "nationality",
    "marital", "status", "single", "married", "passport", "visa",
    
    # Titles & Roles
    "developer", "engineer", "manager", "lead", "consultant", "intern", "fresher",
    "btech", "mtech", "bsc", "msc", "phd", "bachelor", "master", "university", "college",
    "school", "institute", "student", "graduate", "candidate", "applicant",
    
    # Institutions & Education (Fix for "Nehru Vidhyasalai HSS")
    "hss", "school", "college", "university", "institute", "academy", "vidyalaya", "vidhyasalai",
    "matriculation", "secondary", "primary", "high", "campus",
    
    # Project & Tech terms (Fix for "Apriori Algorithm Technologies")
    "algorithm", "technologies", "technology", "system", "analysis", "data", "science",
    "application", "project", "tool", "framework", "library", "software", "solution",
    
    # Common Junk
    "gmail", "com", "org", "net", "edu", "in", "us", "uk", "www", "http", "https",
    "email", "phone", "mobile", "address", "location", "city", "state", "country",
    "page", "pageof", "curriculumvitae", "resumepdf"
}

# Blocklist for Locations (Fix for "Node.js", "React" as GPE)
LOCATION_BLOCKLIST = {
    "node", "node.js", "react", "react.js", "python", "java", "sql", "html", "css",
    "aws", "azure", "google", "microsoft", "ibm", "oracle", "sap",
    "english", "tamil", "hindi", "german", "french", "spanish",
    "remote", "onsite", "hybrid", "available", "immediately"
}

# Common Section Headers (to stop extraction)
SECTION_HEADERS = {
    "education", "experience", "work experience", "projects", "skills", "technical skills",
    "certifications", "certificates", "achievements", "languages", "interests", "hobbies", 
    "references", "declaration", "summary", "profile", "objective"
}

def normalize_tag(user_tag: str) -> str:
    """
    Convert a user-provided tag into a system tag (NER label or Pattern key).
    """
    cleaned_tag = user_tag.lower().strip()
    
    # Direct lookup
    if cleaned_tag in TAG_MAPPINGS:
        return TAG_MAPPINGS[cleaned_tag]
    
    # Fuzzy / substring matching (simple rule-based)
    for key, value in TAG_MAPPINGS.items():
        if key in cleaned_tag:
            return value
            
    # Universal Fallback: Treat any unknown tag as a Keyword to search for
    # e.g. User asks for "Passport No" -> System looks for "Passport No" in text
    return f"KEYWORD:{cleaned_tag}"

def clean_location_entities(locations: list) -> list:
    """
    Filter common technical terms often misclassified as GPE (Location).
    """
    valid_locs = []
    seen = set()
    for loc in locations:
        clean_loc = loc.lower().strip()
        # Filter blocklist
        if clean_loc in LOCATION_BLOCKLIST:
            continue
        # Filter if it's in NAME blocklist (often overlap with tech terms)
        if clean_loc in NAME_BLOCKLIST:
            continue
        
        if clean_loc not in seen:
            valid_locs.append(loc)
            seen.add(clean_loc)
            
    return valid_locs

def get_best_candidate_name(persons: list, full_text: str) -> str:
    """
    Select the best candidate name.
    1. First Line Heuristic (Most reliable for resumes).
    2. Fallback to NER (PERSON entities), prioritized by position and quality.
    """
    # --- Strategy 1: Top Lines Heuristic ---
    # Check top 5 lines for Name patterns or capitalized lines
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    
    # 1. Look for explicit prefixes in top lines
    for i in range(min(len(lines), 10)):
        line = lines[i]
        # Check specific prefixes
        match = re.match(r"(?i)^(Name|Candidate Name|Student Name)\s*[:|-]?\s*(.+)", line)
        if match:
            possible_name = match.group(2).strip()
            # Basic validation
            if len(possible_name.split()) >= 2 and not any(char.isdigit() for char in possible_name):
                 return possible_name.title()

    # 2. Fallback: Check top 3 lines for standalone capitalized text
    if lines:
        for i in range(min(len(lines), 3)):
            line = lines[i]
            tokens = line.split()
            
            # 1. Length check (2-4 words usually)
            if 2 <= len(tokens) <= 5:
                # 2. Blocklist check on parts
                is_blocked = False
                for t in tokens:
                    clean_t = t.lower().strip(r'.,|:-')
                    if clean_t in NAME_BLOCKLIST:
                        is_blocked = True
                        break
                
                # 3. Digit/Email check
                if not is_blocked and not re.search(r'\d', line) and '@' not in line:
                    # Additional check: ensure it's not all lowercase (unless fuzzy)
                    # and mostly letters.
                    return line.title()

    # --- Strategy 2: NER Logic (Fallback) ---
    if not persons:
        return "Not found"
    
    valid_names = []
    lower_full_text = full_text.lower()
    
    for p in persons:
        clean_p = p.lower().strip()
        tokens = clean_p.split()
        
        # Filters (Blocklist, Substring, Length, Numeric)
        if clean_p in NAME_BLOCKLIST: continue
        if any(t in NAME_BLOCKLIST for t in tokens): continue
        if len(clean_p) < 3: continue
        if re.search(r'\d', p) or '@' in p: continue
            
        # Preference: Multi-Word & Top of Doc
        is_multi_word = len(tokens) >= 2
        start_index = lower_full_text.find(clean_p)
        is_at_top = start_index != -1 and start_index < 800 # Relaxed to 800 chars
        
        score = 0
        if is_multi_word: score += 2
        if is_at_top: score += 3 # Top preference is stronger
        
        valid_names.append((p, score, start_index))
        
    if not valid_names:
        return "Not found"
    
    # Sort by Score (Desc), then by Start Position (Asc)
    valid_names.sort(key=lambda x: (-x[1], x[2]))
    
    return valid_names[0][0]

def clean_skills_list(text_chunk: str) -> list:
    """
    Clean a raw string of skills into a nice list.
    Splits by commas, bullets, newlines.
    """
    # 1. Replace bullets and common delimiters with a standard comma
    cleaned = re.sub(r'[•●\-\*➤\n]', ',', text_chunk)
    
    # 2. Split by comma
    items = cleaned.split(',')
    
    # 3. Clean each item
    final_skills = []
    for item in items:
        item = item.strip()
        # Remove empty items and items that are just punctuation
        if item and len(item) > 1 and not re.match(r'^[\W_]+$', item):
            final_skills.append(item)
            
    # 4. Deduplicate while preserving order
    seen = set()
    deduped = []
    for x in final_skills:
        if x.lower() not in seen:
            deduped.append(x)
            seen.add(x.lower())
            
    return deduped

def extract_simple_key_value(text: str, key_type: str) -> str:
    """
    Extract specific single-line values like "Invoice Number: 123" using regex.
    """
    patterns = []
    
    if key_type == "invoice_number":
        patterns = [
            r"(?i)Invoice\s*N[o0]\s*[-.:]?\s*([A-Za-z0-9/-]+)",  # Invoice No : 123
            r"(?i)Bill\s*N[o0]\s*[-.:]?\s*([A-Za-z0-9/-]+)",      # Bill No : 123
            r"(?i)Invoice\s*#\s*([A-Za-z0-9/-]+)",            # Invoice # 123
        ]
    elif key_type == "amount":
        patterns = [
            r"(?i)Total\s*Amount\s*[-.:]?\s*([\d,]+\.?\d*)",
            r"(?i)Grand\s*Total\s*[-.:]?\s*([\d,]+\.?\d*)",
            r"(?i)Net\s*Amount\s*[-.:]?\s*([\d,]+\.?\d*)",
        ]
    elif key_type == "gst":
        patterns = [
            r"(?i)GST\s*N[o0]\s*[-.:]?\s*([A-Za-z0-9]+)",
            r"(?i)GSTIN\s*[-.:]?\s*([A-Za-z0-9]+)",
        ]
    elif key_type == "state":
        patterns = [
            r"(?i)STATE\s*[:|-]?\s*([A-Z\s]+)",
        ]
    elif key_type == "state_code":
        patterns = [
            r"(?i)STATE\s*CODE\s*[:|-]?\s*(\d+)",
        ]
    elif key_type == "dob":
        patterns = [
            r"(?i)(?:DOB|Date\s*of\s*Birth|Birth\s*Date)\s*[:|-]?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
            r"(?i)(?:DOB|Date\s*of\s*Birth|Birth\s*Date)\s*[:|-]?\s*([A-Za-z]+\s\d{1,2},?\s\d{4})", # May 12, 1990
        ]
    elif key_type == "id":
        patterns = [
            r"(?i)(?:ID|Roll|Reg|Enrollment)\s*(?:No|Number|Num)?\s*[:|-]?\s*([A-Za-z0-9/-]+)",
            r"(?i)Student\s*ID\s*[:|-]?\s*([A-Za-z0-9/-]+)",
        ]
        
    for pat in patterns:
        match = re.search(pat, text)
        if match:
            # Clean up the result (remove pipes or trailing junk if regex overshot)
            return match.group(1).split('|')[0].strip()
            
    return ""

def extract_keyword_section(text: str, keyword: str) -> str:
    """
    Context-Based Extraction:
    Extract text following a keyword (e.g. "Skills") until the next section header.
    """
    lower_text = text.lower()
    keyword = keyword.lower()
    
    # Find the keyword
    # We want to match "Skills:" or "Skills\n" or "Skills" followed by space
    # Simple find matches substrings too easily (e.g. "soft skills" in a sentence)
    # Let's try to find it as a standalone header-like line
    
    start_idx = -1
    
    # Try finding "Keyword\n" or "Keyword:"
    candidates = [f"{keyword}\n", f"{keyword}:", f"{keyword} "]
    for cand in candidates:
         idx = lower_text.find(cand)
         if idx != -1:
             start_idx = idx
             break
             
    if start_idx == -1:
        # Fallback to simple find if strict header not found
        start_idx = lower_text.find(keyword)
        
    if start_idx == -1:
        return ""
        
    # Find the end of the line where keyword appears (skip the header itself)
    header_end = text.find('\n', start_idx)
    if header_end == -1:
         return text[start_idx:]
         
    content_start = header_end + 1
    
    # Scan forward to find the NEXT section header
    # We will search for known headers occurring at the start of a line
    
    relevant_text_end = len(text)
    
    # Look for double newlines as a safe fallback limit
    double_newline = text.find("\n\n", content_start) # Optional heuristic
    
    # Iterate through possible next headers
    first_next_header_idx = len(text)
    
    for header in SECTION_HEADERS:
        # Don't stop at the same header we are extracting
        if header in keyword: 
            continue
            
        # Search for "\nHeader" or "\nHeader:"
        # This prevents matching "I have experience in..."
        # We search case-insensitive
        
        # Regex is safer for word boundaries, but simple search is faster/easier here
        # We manually check common formatting
        
        # Construct search patterns for next header
        patterns_to_check = [f"\n{header}", f"\n{header}:"]
        
        for pat in patterns_to_check:
            found = lower_text.find(pat, content_start)
            if found != -1 and found < first_next_header_idx:
                first_next_header_idx = found
                
    # If we found a next header, that's our limit
    if first_next_header_idx < len(text):
        relevant_text_end = first_next_header_idx
    elif double_newline != -1 and double_newline > content_start + 20: 
        # If no header found, but there's a paragraph break reasonable far away, use it
        # +20 avoids stopping immediately if the section starts with a blank line
        # This is a fallback.
        pass 
        
    raw_content = text[content_start:relevant_text_end].strip()
    return raw_content

def map_tags_to_values(user_tags: list, ner_entities: dict, patterns: dict, full_text: str) -> dict:
    """
    Map user tags to extracted values based on the normalized system tag.
    """
    results = {}
    
    for tag in user_tags:
        system_tag = normalize_tag(tag)
        
        # Case 1: Regex Pattern Match
        if system_tag.startswith("PATTERN:"):
            pattern_key = system_tag.split(":")[1]
            if pattern_key == "url":
                urls = patterns.get("url", [])
                tag_lower = tag.lower()
                filtered_urls = []
                if "linkedin" in tag_lower:
                    filtered_urls = [u for u in urls if "linkedin" in u.lower()]
                elif "github" in tag_lower:
                    filtered_urls = [u for u in urls if "github" in u.lower()]
                else:
                    filtered_urls = urls
                results[tag] = filtered_urls if filtered_urls else "Not found"
            else:
                values = patterns.get(pattern_key, [])
                results[tag] = values[0] if values else "Not found"

        # Case 2: NER Entity Match (PERSON, ORG, GPE)
        elif system_tag in ner_entities:
            matches = ner_entities.get(system_tag, [])
            
            if system_tag == "PERSON":
                 # Use improved name extractor
                 name = get_best_candidate_name(matches, full_text)
                 results[tag] = name if name else "Not found"
                 
            elif system_tag == "GPE":
                # Use improved location cleaner
                locations = clean_location_entities(matches)
                results[tag] = locations if locations else "Not found"
                
            else:
                # For basic entities, join unique ones or list them
                unique_matches = list(set(matches))
                results[tag] = unique_matches if unique_matches else "Not found"
            
        # Case 3: Keyword Search (Skills, Education, etc.)
        elif system_tag.startswith("KEYWORD:"):
            keyword_key = system_tag.split(":")[1]
            
            # Special handling for "skills" to return a list
            if keyword_key == "skills":
                raw_text = extract_keyword_section(full_text, "skill") # search for "skill" or "skills"
                if raw_text:
                    results[tag] = clean_skills_list(raw_text)
                else:
                     results[tag] = "Not found" # Return explicitly not found if empty
            else:
                # Generic fallback for Education, Projects, etc.
                extracted = extract_keyword_section(full_text, keyword_key)
                results[tag] = extracted if extracted else "Not found"
        
        # Case 4: Key-Value Extraction (Invoice No, Amount, etc.)
        elif system_tag.startswith("KEY_VALUE:"):
            kv_key = system_tag.split(":")[1]
            extracted_val = extract_simple_key_value(full_text, kv_key)
            results[tag] = extracted_val if extracted_val else "Not found"
                
        else:
            results[tag] = "Not found" # Default for unrecognized tags
            
    return results
