import json
import os

# -----------------
# Dateipfad für Speicherung
# -----------------
SAVE_FILE = "mindmap.json"

# -----------------
# Lade Mindmap oder erstelle neue
# -----------------
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        mindmap_data = json.load(f)
else:
    mindmap_data = {"name": "OSINT", "children": []}

# -----------------
# HTML Template mit verbessertem Design
# -----------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>OSINT Mindmap</title>
<style>
body {
    font-family: 'Monospace', monospace;
    background: #1e1e1e;
    color: #c5c8c6;
    margin: 0;
    padding: 20px;
}
h1 {
    text-align: center;
    color: #8abeb7;
    margin-bottom: 30px;
    font-weight: normal;
}
#mindmap {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    font-size: 14px;
}
.node {
    position: relative;
    background: #282a2e;
    color: #c5c8c6;
    padding: 6px 12px 6px 36px; /* Platz für Toggle-Button */
    border-left: 3px solid #8abeb7;
    cursor: pointer;
    margin: 4px 0;
    border-radius: 3px;
    transition: background 0.2s, transform 0.1s;
}
.node:hover {
    background: #373b41;
}
.children {
    margin-left: 20px;
    overflow: hidden;
    max-height: 0;
    transition: max-height 0.3s ease;
}
.node.open > .children {
    max-height: 1000px;
}
.toggle {
    position: absolute;
    left: 6px; 
    top: 50%;
    transform: translateY(-50%);
    width: 22px;       
    height: 22px;      
    background: #1e1e1e;
    border: 2px solid #8abeb7;
    border-radius: 50%;
    text-align: center;
    line-height: 18px; 
    font-size: 14px;   
    color: #8abeb7;
    cursor: pointer;
    font-weight: bold;
    transition: background 0.2s, transform 0.1s;
}
.toggle:hover {
    background: #373b41;
    transform: scale(1.1);
}
</style>
</head>
<body>
<h1>OSINT Mindmap</h1>
<div id="mindmap"></div>
<script>
let data = {mindmap_json};

function renderNode(node) {
    const div = document.createElement("div");
    div.className = "node";

    if(node.children && node.children.length > 0) {
        const toggle = document.createElement("div");
        toggle.className = "toggle";
        toggle.textContent = "+";
        toggle.onclick = (e) => {
            e.stopPropagation();
            div.classList.toggle("open");
            toggle.textContent = div.classList.contains("open") ? "−" : "+";
        };
        div.appendChild(toggle);
    }

    // Textspan rechts neben Button
    const text = document.createElement("span");
    text.style.marginLeft = "4px"; // Abstand zwischen Button und Text
    text.textContent = node.name;
    div.appendChild(text);

    if(node.children && node.children.length > 0) {
        const childrenDiv = document.createElement("div");
        childrenDiv.className = "children";
        node.children.forEach(child => {
            childrenDiv.appendChild(renderNode(child));
        });
        div.appendChild(childrenDiv);
    }

    return div;
}

function refresh() {
    const container = document.getElementById("mindmap");
    container.innerHTML = "";
    container.appendChild(renderNode(data));
}

refresh();
</script>
</body>
</html>
"""





# -----------------
# Hilfsfunktionen
# -----------------
def save_json():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(mindmap_data, f, ensure_ascii=False, indent=2)

def write_html():
    html_content = HTML_TEMPLATE.replace("{mindmap_json}", json.dumps(mindmap_data, ensure_ascii=False))
    with open("mindmap.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML-Datei aktualisiert: mindmap.html")

def add_node(path, name):
    node = mindmap_data
    for p in path:
        found = False
        for child in node["children"]:
            if child["name"] == p:
                node = child
                found = True
                break
        if not found:
            new_child = {"name": p, "children": []}
            node["children"].append(new_child)
            node = new_child
    node["children"].append({"name": name, "children": []})
    save_json()
    write_html()

def delete_node(path, name):
    node = mindmap_data
    if not path:
        for i, child in enumerate(node["children"]):
            if child["name"] == name:
                node["children"].pop(i)
                save_json()
                write_html()
                return True
        return False
    for p in path:
        found = False
        for child in node["children"]:
            if child["name"] == p:
                node = child
                found = True
                break
        if not found:
            return False
    for i, child in enumerate(node["children"]):
        if child["name"] == name:
            node["children"].pop(i)
            save_json()
            write_html()
            return True
    return False

def print_tree(node=None, prefix=""):
    if node is None:
        node = mindmap_data
    print(prefix + node["name"])
    for child in node["children"]:
        print_tree(child, prefix + "  → ")

# -----------------
# Interaktive Konsole
# -----------------
def main():
    write_html()
    print("Interaktiver OSINT Mindmap Editor")
    print("Mindmap wird in mindmap.html aktualisiert.")
    while True:
        print("\nAktueller Baum:")
        print_tree()
        print("\nOptionen:")
        print("1. Knoten hinzufügen")
        print("2. Knoten löschen")
        print("3. Beenden")
        choice = input("Wähle eine Option: ").strip()
        if choice == "1":
            path_str = input("Pfad zum Elternknoten (z.B. OSINT/Email/Header) oder leer für Root: ").strip()
            path = [p.strip() for p in path_str.split("/")] if path_str else []
            name = input("Name des neuen Knotens: ").strip()
            if name:
                add_node(path, name)
        elif choice == "2":
            path_str = input("Pfad zum Elternknoten des zu löschenden Knotens (z.B. OSINT/Email/Header) oder leer für Root: ").strip()
            path = [p.strip() for p in path_str.split("/")] if path_str else []
            name = input("Name des zu löschenden Knotens: ").strip()
            if name:
                success = delete_node(path, name)
                if success:
                    print(f"Knoten '{name}' wurde gelöscht.")
                else:
                    print(f"Knoten '{name}' nicht gefunden.")
        elif choice == "3":
            print("Beende Editor.")
            break
        else:
            print("Ungültige Option!")

if __name__ == "__main__":
    main()
