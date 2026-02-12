from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://ess.abimm.com/ABIMM_ASP/Request.aspx")
    
    # Save HTML
    with open("venue_page.html", "w", encoding="utf-8") as f:
        f.write(page.content())
        
    print("Page title:", page.title())
    
    # List all buttons and inputs to see what's available
    params = page.evaluate("""() => {
        const inputs = Array.from(document.querySelectorAll('input')).map(i => ({tag: 'input', type: i.type, id: i.id, name: i.name, value: i.value, placeholder: i.placeholder}));
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({tag: 'button', text: b.innerText, id: b.id}));
        return {inputs, buttons};
    }""")
    print("Inputs/Buttons found:", params)
    
    browser.close()
