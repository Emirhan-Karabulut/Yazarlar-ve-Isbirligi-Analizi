import pandas as pd
import ast
from pyvis.network import Network

class Author:
    def __init__(self, orcid, author_name, author_position, coauthors, paper_title):
        self.orcid = orcid
        self.author_name = author_name
        self.author_position = [int(author_position)]
        self.coauthors = [coauthors]
        self.paper_titles = [paper_title]
        self.total_papers = 1

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.connections = set()
        self.size = 15
        self.color = "#00BFFF"
        self.border_color = "#ffffff"
        self.title = ""
        self.authored_papers = []

    def set_attributes(self, total_papers, avg_papers, threshold, paper_titles):
        if total_papers > (avg_papers + threshold):
            self.size = 35
            self.color = "#FFD700"
        self.authored_papers = paper_titles


    def add_connection(self, other_node_id):
        self.connections.add(other_node_id)

class Edge:
    def __init__(self, source_id, target_id):
        self.source = source_id
        self.target = target_id
        self.color = "#ffffff"
        self.opacity = 0.3
        self.weight = 1  
        self.title = ""

    def set_attributes(self,weight=1):
        self.color = "#ffffff"
        self.opacity = 0.3 + (min(weight, 5) * 0.1)
        self.weight = weight
        self.title = f"İşbirliği Sayısı: {weight}"

file_path = "C:/proje_java/veriler.xlsx"
read_data = pd.read_excel(file_path)

unique_authors = []
eşsizIndex = 0
makalesayi = []
toplam_isbirligi_sayi = []
isbirligi_agirligi = []

for i in range(len(read_data)):
    current_orcid = read_data.loc[i, 'orcid']
    if i > 0 and current_orcid == read_data.loc[i - 1, 'orcid']:
        unique_authors[eşsizIndex].author_position.append(int(read_data.loc[i, 'author_position']))
        unique_authors[eşsizIndex].coauthors.append(ast.literal_eval(read_data.loc[i, 'coauthors']))
        unique_authors[eşsizIndex].paper_titles.append(read_data.loc[i, 'paper_title'])
        unique_authors[eşsizIndex].total_papers += 1
        makalesayi[eşsizIndex] += 1
        continue
    else:
        unique_authors.append(Author(read_data.loc[i, 'orcid'], read_data.loc[i, 'author_name'], read_data.loc[i, 'author_position'], ast.literal_eval(read_data.loc[i, 'coauthors']), read_data.loc[i, 'paper_title']))
        eşsizIndex = len(unique_authors) - 1
        if eşsizIndex >= len(makalesayi):
            makalesayi.append(0)
        makalesayi[eşsizIndex] += 1

for i in range(len(unique_authors)):
    for y in range(len(unique_authors[i].coauthors)):
        try:
            index = int(unique_authors[i].author_position[y]) - 1
            if 0 <= index < len(unique_authors[i].coauthors[y]):
                unique_authors[i].coauthors[y].pop(index)
        except Exception as e:
            print(f"Hata oluştu: {e} - Yazar {i+1}, Paper {y+1}")

for i in range (0,eşsizIndex):
    unique_coauthors = set()
    for coauthor_list in unique_authors[i].coauthors:
        unique_coauthors.update(coauthor_list)

    toplam_isbirligi_sayi.append(len(unique_coauthors))
    
nodes = {}
edges = []
edge_weights = {}

for author in unique_authors:
    nodes[author.orcid] = Node(author.orcid, author.author_name)

for author in unique_authors:
    for coauthor_list in author.coauthors:
        for coauthor_name in coauthor_list:
            coauthor_orcid = next((a.orcid for a in unique_authors if a.author_name == coauthor_name), None)
            if coauthor_orcid:
                if coauthor_orcid not in nodes:
                    nodes[coauthor_orcid] = Node(coauthor_orcid, coauthor_name)
                
                if coauthor_orcid != author.orcid:
                    edge_key = f"{min(author.orcid, coauthor_orcid)}-{max(author.orcid, coauthor_orcid)}"
                    
                    if edge_key in edge_weights:
                        edge_weights[edge_key] += 1
                    else:
                        edge_weights[edge_key] = 1
                        nodes[author.orcid].connections.add(coauthor_orcid)
                        nodes[coauthor_orcid].connections.add(author.orcid)
                        edges.append(Edge(author.orcid, coauthor_orcid))
            else:
                coauthor_id = f"{coauthor_name}"
                if coauthor_id not in nodes:
                    nodes[coauthor_id] = Node(coauthor_id, coauthor_name)
                
                if coauthor_id != author.orcid:
                    edge_key = f"{min(author.orcid, coauthor_id)}-{max(author.orcid, coauthor_id)}"
                    
                    if edge_key in edge_weights:
                        edge_weights[edge_key] += 1
                    else:
                        edge_weights[edge_key] = 1
                        nodes[author.orcid].connections.add(coauthor_id)
                        nodes[coauthor_id].connections.add(author.orcid)
                        edges.append(Edge(author.orcid, coauthor_id))

def visualize_network():
    net = Network(notebook=False, height="100vh", width="100%", bgcolor="#1a1a1a", font_color="white")
    
    net.set_options("""
    const options = {
        "nodes": {
            "shape": "dot",
            "size": 20,
            "font": {
                "size": 16,
                "face": "Arial",
                "color": "#ffffff",
                "strokeWidth": 10,
                "strokeColor": "#000000"
            },
            "borderWidth": 3,
            "borderWidthSelected": 4,
            "opacity": 0.9,
            "color": {
                "background": "#6FA3EF",
                "border": "#2D79B4"
            },
            "shadow": {
                "enabled": true,
                "color": "rgba(0, 0, 0, 0.2)",
                "size": 10
            }
        },
        "edges": {
            "color": {
                "color": "#C0C0C0",
                "highlight": "#FF0000",
                "opacity": 0.6
            },
            "width": 2,
            "smooth": {
                "enabled": true,
                "type": "continuous",
                "forceDirection": "none"
            },
            "arrows": {
                "to": {
                    "enabled": false,
                    "scaleFactor": 0.5
                }
            }
        },
        "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -150,
                "centralGravity": 0.015,
                "springLength": 250,
                "springConstant": 0.05,
                "damping": 0.4
            },
            "minVelocity": 0.5,
            "solver": "forceAtlas2Based",
            "timestep": 0.5,
            "stabilization": {
                "iterations": 200,
                "updateInterval": 25
            },
            "barnesHut": {
                "gravitationalConstant": -700,
                "centralGravity": 0.1,
                "springLength": 200
            }
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": {
                "enabled": true
            },
            "tooltipDelay": 200,
            "zoomView": true,
            "dragView": true
        },
        "layout": {
            "randomSeed": 2,
            "improvedLayout": true,
            "hierarchical": {
                "enabled": false,
                "levelSeparation": 150,
                "nodeSpacing": 200,
                "treeSpacing": 400
            }
        }
    }
    """)

    avg_papers = sum(author.total_papers for author in unique_authors) / len(unique_authors)
    threshold = avg_papers * 0.2

    coauthor_papers_dict = {}
    for author in unique_authors:
        for i, coauthor_list in enumerate(author.coauthors):
            for coauthor_name in coauthor_list:
                coauthor_orcid = next((a.orcid for a in unique_authors if a.author_name == coauthor_name), None)
                if coauthor_orcid:
                    if coauthor_orcid not in coauthor_papers_dict:
                        coauthor_papers_dict[coauthor_orcid] = []
                    coauthor_papers_dict[coauthor_orcid].append(author.paper_titles[i])
    for author in unique_authors:
        if author.orcid not in nodes:
            nodes[author.orcid] = Node(author.orcid, author.author_name)
        nodes[author.orcid].set_attributes(author.total_papers, avg_papers, threshold, author.paper_titles)

    for node in nodes.values():
        net.add_node(
            node.id,
            label=node.name,
            title=node.name,
            size=node.size,
            color=node.color,
            borderWidth=2,
            borderColor=node.border_color,
            shape='dot'
        )

    for edge in edges:
        edge_key = f"{min(edge.source, edge.target)}-{max(edge.source, edge.target)}"
        weight = edge_weights.get(edge_key, 1)
        edge.set_attributes(weight) 
        net.add_edge(edge.source, edge.target, title=edge.title,width=weight, color={'color': edge.color, 'opacity': edge.opacity})

    net.show("proje3.html", notebook=False)
    html = net.generate_html()

    head_html_content = """
        <style type="text/css">
            .myButton {
                background-color: #4287f5;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 30px;
                transition: background-color 0.3s;
                width: 100px;
                height: 75px;
            }

            .myButton:hover {
                background-color: #3272d9;
            }

            .buttonContainer {
                position: absolute;
                top: 20px;
                right: 20px;
                z-index: 100;
                display: flex;
                flex-direction: column;
            }

            .outputContainer {
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 100;
                background-color:rgb(15, 15, 15);
                color: #fff;
                padding: 20px;
                border-radius: 25px;
                width: 300px;
                height: calc(100vh - 20px);
                overflow-y: auto;
                box-shadow: 0 4px 8px rgba(255, 10, 10, 0.1);
            }
            .searchBox {
                position: fixed;
                top: 8%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: #333;
                padding: 20px;
                border-radius: 10px;
                z-index: 1000;
                display: none;
                width:500;
            }
            .searchBox input {
                padding: 8px;
                margin-right: 10px;
                border-radius: 4px;
                border: 1px solid #666;
            }
            .searchBox button {
                padding: 8px 16px;
                background-color: #4287f5;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .closeButton {
                position: absolute;
                top: 8px;
                right: 8px;
                background: none;
                border: none;
                color: #999;
                cursor: pointer;
                font-size: 20px;
                padding: 5px;
                line-height: 1;
                transition: color 0.2s;
            }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>

        """
    html = html.replace("</head>", head_html_content + "</head>")

    body_html_content = """
        <div class="card" style="width: 100%">
            <div class="buttonContainer">
                <button class="myButton" onclick="showOutput(1, 'case1')">1. İster</button>
                <button class="myButton" onclick="showOutput(2, 'case2')">2. İster</button>
                <button class="myButton" onclick="showOutput(3, 'case3')">3. İster</button>
                <button class="myButton" onclick="showOutput(4, 'case4')">4. İster</button>
                <button class="myButton" onclick="showOutput(5, 'case5')">5. İster</button>
                <button class="myButton" onclick="showOutput(6, 'case6')">6. İster</button>
                <button class="myButton" onclick="showOutput(7, 'case7')">7. İster</button>
            </div>
            <div class="outputContainer" id="outputContainer">Çıktı Burada Gözükecek...</div>
        </div>
            <div id="authorSearchBox" class="searchBox">
                <button class="closeButton" onclick="closeSearchBox()">×</button>
            </div>
        <script type="text/javascript">
            let searchContext = '';
        
        function showSearchBox(context) {
            searchContext = context;
            const searchBox = document.getElementById('authorSearchBox');
            
            if (context === 'case1') {
                searchBox.innerHTML = `
                    <button class="closeButton" onclick="closeSearchBox()">×</button>
                    <input type="text" id="startAuthorId" placeholder="Başlangıç Yazar ID">
                    <input type="text" id="endAuthorId" placeholder="Hedef Yazar ID">
                    <button onclick="searchAuthors()">Ara</button>
                `;
            } else {
                searchBox.innerHTML = `
                    <button class="closeButton" onclick="closeSearchBox()">×</button>
                    <input type="text" id="authorIdInput" placeholder="Yazar Orcid'i Giriniz">
                    <button onclick="searchAuthor()">Ara</button>
                `;
            }
            
            searchBox.style.display = 'block';
        }

        function closeSearchBox() {
            document.getElementById('authorSearchBox').style.display = 'none';
        }

        function searchAuthor() {
            const authorId = document.getElementById('authorIdInput').value;
            if (!authorId) {
                alert("Lütfen Bir Yazar Orcid'i Giriniz");
                return;
            }
            if (searchContext === 'case2') {
                createQueue(authorId);
            } else if (searchContext === 'case4') {
                calculateAllShortestPaths(authorId);
            } else if (searchContext === 'case5') {
                analyzeCollaborations(authorId);
            } else if (searchContext === 'case7') {
                findLongestPath(authorId);
            }
            closeSearchBox();
        }
        
        let authorQueue = [];
        let bstRoot = null;
        let isExpanded = false;
        let originalStyles = {};

        class BSTNode {
            constructor(authorId, authorName, paperCount) {
                this.authorId = authorId;
                this.authorName = authorName;
                this.paperCount = paperCount;
                this.left = null;
                this.right = null;
                this.x = 0;
                this.y = 0;
            }
        }

        let p5Instance = null;

        function searchAuthors() {
            const startId = document.getElementById('startAuthorId').value;
            const endId = document.getElementById('endAuthorId').value;
            
            if (!startId || !endId) {
                alert("Lütfen Her İki Yazar Orcid'ini de Girin!");
                return;
            }
            
            authorQueue = [];
            
            const path = findShortestPath(startId, endId);
            if (path) {
                path.forEach(nodeId => {
                    const node = nodes.get(nodeId);
                    const paperCount = node.authored_papers ? node.authored_papers.length : 0;
                    authorQueue.push({ id: nodeId, name: node.label, papers: paperCount});
                });
                alert("Kuyruk Oluşturuldu! 3. İsteri Kullanarak BST İşlemlerini Gerçekleştirebilirsiniz.");
                closeSearchBox();
            } else {
                alert("Yol bulunamadı! Kuyruk oluşturulamadı.");
            }
        }

        function findShortestPath(startId, endId) {

            const outputContainer = document.getElementById('outputContainer');
            
            const startNode = nodes.get(startId);
            const endNode = nodes.get(endId);
            
            if (!startNode || !endNode) {
                outputContainer.innerHTML = "Bir veya iki yazar ID'si bulunamadı!";
                return null;
            }

            let distances = {};
            let previous = {};
            let queue = [];
            let path = [];
            let queueSteps = [];
            
            nodes.get().forEach(node => {
                distances[node.id] = Infinity;
                previous[node.id] = null;
                queue.push(node.id);
            });
            distances[startId] = 0;
            
            outputContainer.innerHTML = `
                <h3>En Kısa Yol Arama</h3>
                <p><strong>Başlangıç:</strong> ${startNode.label}</p>
                <p><strong>Hedef:</strong> ${endNode.label}</p>
                <div id="queueSteps"></div>
                <div id="pathResult"></div>
            `;

            while (queue.length > 0) {
                let minDistance = Infinity;
                let minNode = null;
                
                queue.forEach(nodeId => {
                    if (distances[nodeId] < minDistance) {
                        minDistance = distances[nodeId];
                        minNode = nodeId;
                    }
                });
                
                if (minNode === null) break;
                
                queueSteps.push(`${nodes.get(minNode).label} işleniyor...`);
                
                if (minNode === endId) break;
                
                queue = queue.filter(id => id !== minNode);
                
                edges.get().forEach(edge => {
                    if (edge.from === minNode || edge.to === minNode) {
                        const neighbor = edge.from === minNode ? edge.to : edge.from;
                        if (queue.includes(neighbor)) {
                            const weight = parseInt(edge.title.match(/İşbirliği Sayısı: (\d+)/)[1]);
                            const distance = distances[minNode] + weight;
                            
                            if (distance < distances[neighbor]) {
                                distances[neighbor] = distance;
                                previous[neighbor] = minNode;
                            }
                        }
                    }
                });
            }
            
            let current = endId;
            while (current !== null) {
                path.unshift(current);
                current = previous[current];
            }
            
            let queueContent = document.getElementById('queueSteps');
            queueSteps.forEach((step, index) => {
                setTimeout(() => {
                    queueContent.innerHTML += `<p>${step}</p>`;
                }, 1 * index);
            });
            
            setTimeout(() => {
                const pathContent = document.getElementById('pathResult');
                if (path.length > 1) {
                    const pathLabels = path.map(id => nodes.get(id).label);
                    pathContent.innerHTML = `
                        <h4>Bulunan En Kısa Yol:</h4>
                        <p>${pathLabels.join(' -> ')}</p>
                        <p>Toplam Mesafe: ${distances[endId]}</p>
                    `;
                    highlightPath(previous, startId, endId);
                } else {
                    pathContent.innerHTML = "<p>İki yazar arasında bağlantı bulunamadı!</p>";
                }
            }, 1 * queueSteps.length);

            return path.length > 1 ? path : null;
        }

        function highlightPath(previous, startId, endId) {
            const originalEdgeStyles = edges.get().map(edge => ({
                id: edge.id,
                color: edge.color,
                width: edge.width
            }));
            
            edges.get().forEach(edge => {
                edges.update({id: edge.id, color: {color: '#ffffff', opacity: 0.5}});
            });
            
            let highlightedEdgeIds = [];
            let current = endId;
            while (previous[current] !== null) {
                const prev = previous[current];
                edges.get().forEach(edge => {
                    if ((edge.from === prev && edge.to === current) ||
                        (edge.from === current && edge.to === prev)) {
                        edges.update({
                            id: edge.id, 
                            color: {color: '#e900ff', highlight: '#ff00ff', opacity: 1}, 
                            width: 3
                        });
                        highlightedEdgeIds.push(edge.id);
                    }
                });
                current = prev;
            }
            
            setTimeout(() => {
                originalEdgeStyles.forEach(style => {
                    edges.update({
                        id: style.id,
                        color: style.color,
                        width: style.width
                    });
                });
            }, 30000);
        }

        function createQueue(authorId) {
            const outputContainer = document.getElementById('outputContainer');
            let queue = [];

            edges.get().forEach(edge => {
                if (edge.from === authorId || edge.to === authorId) {
                    let weight = parseInt(edge.title.match(/İşbirliği Sayısı: (\d+)/)[1]);
                    let collaboratorId = edge.from === authorId ? edge.to : edge.from;
                    let collaborator = nodes.get(collaboratorId);
                    queue.push({ id: collaborator.id, name: collaborator.label, weight: weight });
                }
            });

            for (let i = 0; i < queue.length - 1; i++) {
                for (let j = 0; j < queue.length - i - 1; j++) {
                    if (queue[j].weight < queue[j + 1].weight) {
                        let temp = queue[j];
                        queue[j] = queue[j + 1];
                        queue[j + 1] = temp;
                    }
                }
            }

            const authorNode = nodes.get(authorId);
            const authorName = authorNode ? authorNode.label : "Unknown Author";

            outputContainer.innerHTML = `
                <h3>İşbirliği Kuyruğu</h3>
                <p><strong>Yazar:</strong> ${authorName}</p>
                <p><strong>Yazar Orcid:</strong> ${authorId}</p>
                <p><strong>Kuyruk:</strong></p>
                <ul>
                    ${queue.map(item => `<li>${item.name} (ID: ${item.id}, Collab Count: ${item.weight})</li>`).join('')}
                </ul>
            `;

            let currentQueue = queue.slice();
            currentQueue.forEach((item, index) => {
                setTimeout(() => {
                    outputContainer.innerHTML += `<p>${item.name} kuyruğa eklendi.</p>`;
                }, 1000 * index);
            });

        function dequeueElements(queue) {
                if (queue.length > 0) {
                    const removed = queue.shift();
                    outputContainer.innerHTML += `<p>${removed.name} kuyruktan çıkarıldı.</p>`;
                    setTimeout(() => dequeueElements(queue), 1000);
                }
            }

            setTimeout(() => dequeueElements(currentQueue), 1000 * queue.length + 2000);
        }

        function createBSTFromQueue() {
            bstRoot = null;
            authorQueue.forEach(author => {
                bstRoot = insertIntoBST(bstRoot, author.id, author.name, author.papers);
            });
        }

        function insertIntoBST(node, authorId, authorName, paperCount) {
            if (node === null) {
                return new BSTNode(authorId, authorName, paperCount);
            }
            
            if (paperCount > node.paperCount) {
                node.right = insertIntoBST(node.right, authorId, authorName, paperCount);
            }
            else if (paperCount <= node.paperCount) {
                node.left = insertIntoBST(node.left, authorId, authorName, paperCount);
            }
            
            return node;
        }

        function removeFromBST(node, authorId) {
            if (node === null) {
                return null;
            }

            if (authorId === node.authorId) {
                if (node.left === null && node.right === null) {
                    return null;
                }
                if (node.left === null) {
                    return node.right;
                }
                if (node.right === null) {
                    return node.left;
                }
                let successor = findMin(node.right);
                node.authorId = successor.authorId;
                node.authorName = successor.authorName;
                node.paperCount = successor.paperCount;
                node.right = removeFromBST(node.right, successor.authorId);
            }

            return node;
        }

        function findNodeByAuthorId(node, authorId) {
            if (node === null || node.authorId === authorId) {
                return node;
            }
            
            const leftResult = findNodeByAuthorId(node.left, authorId);
            if (leftResult !== null) {
                return leftResult;
            }
            
            return findNodeByAuthorId(node.right, authorId);
        }

        function findMin(node) {
            if (node === null) return null;
            let current = node;
            while (current.left !== null) {
                current = current.left;
            }
            return current;
        }

        function processBSTOperation() {
            const authorId = document.getElementById('bstAuthorId').value;
            if (!authorId) {
                alert("Lütfen bir yazar ID'si girin!");
                return;
            }
            
            const authorExists = authorQueue.some(author => author.id === authorId);
            if (!authorExists) {
                alert("Bu yazar kuyruğa ait değil!");
                return;
            }
            
            authorQueue = authorQueue.filter(author => author.id !== authorId);
            
            rebuildBST();
        }

        function rebuildBST() {
            bstRoot = null;
            
            if (authorQueue.length > 0) {
                createBSTFromQueue();
            }
            
            displayBST();
        }

        function toggleContainerSize() {
            const outputContainer = document.getElementById('outputContainer');
            const toggleButton = document.getElementById('toggleSizeBtn');
            isExpanded = !isExpanded;

            if (isExpanded) {
                if (!originalStyles.width) {
                    originalStyles = {
                        width: outputContainer.style.width,
                        height: outputContainer.style.height,
                        overflow: outputContainer.style.overflow,
                        transition: outputContainer.style.transition
                    };
                }
                
                outputContainer.style.width = '1500px';
                outputContainer.style.height = '800px';
                outputContainer.style.overflow = 'auto';
                outputContainer.style.transition = 'all 0.3s ease';
                toggleButton.style.background = '#e53e3e';
                toggleButton.innerHTML = '⤡';
            } else {
                outputContainer.style.width = originalStyles.width;
                outputContainer.style.height = originalStyles.height;
                outputContainer.style.overflow = originalStyles.overflow;
                outputContainer.style.transition = originalStyles.transition;
                toggleButton.style.background = '#4299e1';
                toggleButton.innerHTML = '⤢';
            }

            if (p5Instance) {
                p5Instance.resizeCanvas(
                    isExpanded ? 1400 : 800,
                    isExpanded ? 700 : 400
                );
                calculateNodePositions(bstRoot, p5Instance.width / 2, 60, p5Instance.width / 2);
            }
        }

        function displayBST() {
            const outputContainer = document.getElementById('outputContainer');
            outputContainer.innerHTML = '';
            
            if (authorQueue.length === 0) {
                outputContainer.innerHTML = "<div style='color: white; text-align: center; padding: 20px;'>Kuyruk boş! BST oluşturulamıyor.</div>";
                outputContainer.style.width = originalStyles.width;
                outputContainer.style.height = originalStyles.height;
                outputContainer.style.overflow = originalStyles.overflow;
                outputContainer.style.transition = originalStyles.transition;
                return;
            }
            
            const controls = document.createElement('div');
            controls.innerHTML = `
                <div style="margin: 10px 0;">
                    <input type="text" id="bstAuthorId" placeholder="Çıkarılacak Yazar ID" style="padding: 5px; margin-right: 10px;">
                    <button onclick="processBSTOperation()" style="padding: 5px 10px;">İşlemi Gerçekleştir</button>
                </div>
            `;
            outputContainer.appendChild(controls);
            
            const toggleButton = document.createElement('button');
            toggleButton.id = 'toggleSizeBtn';
            toggleButton.innerHTML = '⤢';
            toggleButton.style.position = 'absolute';
            toggleButton.style.top = '10px';
            toggleButton.style.right = '10px';
            toggleButton.style.padding = '5px 10px';
            toggleButton.style.background = '#4299e1';
            toggleButton.style.color = 'white';
            toggleButton.style.border = 'none';
            toggleButton.style.borderRadius = '4px';
            toggleButton.style.cursor = 'pointer';
            toggleButton.style.zIndex = '1000';
            toggleButton.style.fontSize = '16px';
            toggleButton.style.width = '30px';
            toggleButton.style.height = '30px';
            toggleButton.style.display = 'flex';
            toggleButton.style.alignItems = 'center';
            toggleButton.style.justifyContent = 'center';
            toggleButton.onclick = toggleContainerSize;
            outputContainer.appendChild(toggleButton);
            
            const canvasContainer = document.createElement('div');
            canvasContainer.id = 'bstCanvas';
            outputContainer.appendChild(canvasContainer);
            
            if (p5Instance) {
                p5Instance.remove();
            }
            
            new p5(sketch, 'bstCanvas');
        }

        const sketch = (p) => {
            const nodeRadius = 40;
            const levelHeight = 100;
            let canvasWidth = isExpanded ? 1400 : 800;
            let canvasHeight = isExpanded ? 700 : 400;
            let hoveredNode = null;
            
            p.setup = () => {
                const canvas = p.createCanvas(canvasWidth, canvasHeight);
                p5Instance = p;
                if (bstRoot) {
                    const initialOffset = canvasWidth * 0.25;
                    calculateNodePositions(bstRoot,canvasWidth / 2,60,initialOffset);
                }
                
                canvas.mousePressed(() => {
                    const clickedNode = findNodeAtPosition(bstRoot, p.mouseX, p.mouseY);
                    if (clickedNode) {
                        copyToClipboard(clickedNode.authorId);
                        showNotification(clickedNode.authorId);
                    }
                });
            };
            
            p.draw = () => {
                p.background('#1a1a1a');
                drawTree(bstRoot);
                
                if (hoveredNode) {
                    p.fill(255);
                    p.noStroke();
                    p.textSize(12);
                    p.text('Kopyalamak için tıklayın', hoveredNode.x, hoveredNode.y - 45);
                }
            };

            p.mouseMoved = () => {
                hoveredNode = findNodeAtPosition(bstRoot, p.mouseX, p.mouseY);
            };

        function calculateNodePositions(node, x, y, offset) {
            if (!node) return;
            
            node.x = x;
            node.y = y;
            
            const minSpacing = 80;
            const levelSpacing = Math.max(minSpacing, offset);
            
            if (node.left) {
                calculateNodePositions(node.left, x - levelSpacing, y + levelHeight, levelSpacing / 2);
            }
            if (node.right) {
                calculateNodePositions(node.right, x + levelSpacing, y + levelHeight, levelSpacing / 2);
            }
        }

        function findNodeAtPosition(node, x, y) {
            if (!node) return null;
            
            const distance = p.dist(x, y, node.x, node.y);
            if (distance < nodeRadius) {
                return node;
            }
            
            const leftResult = findNodeAtPosition(node.left, x, y);
            if (leftResult) return leftResult;
            
            return findNodeAtPosition(node.right, x, y);
        }
        
        function drawTree(node) {
            if (!node) return;
            
            if (node.left) {
                p.stroke('#4a5568');
                p.strokeWeight(3);
                p.line(node.x, node.y, node.left.x, node.left.y);
            }
            if (node.right) {
                p.stroke('#4a5568');
                p.strokeWeight(3);
                p.line(node.x, node.y, node.right.x, node.right.y);
            }
            
            p.noStroke();
            const gradient = p.drawingContext.createRadialGradient(
                node.x, node.y, 0,
                node.x, node.y, nodeRadius
            );
            gradient.addColorStop(0, '#2d3748');
            gradient.addColorStop(1, '#1a202c');
            p.drawingContext.fillStyle = gradient;
            p.circle(node.x, node.y, nodeRadius * 2);
            
            if (hoveredNode === node) {
                p.stroke('#63b3ed');
                p.strokeWeight(4);
            } else {
                p.stroke('#4299e1');
                p.strokeWeight(3);
            }
            p.noFill();
            p.circle(node.x, node.y, nodeRadius * 2);
            
            p.noStroke();
            p.fill(255);
            p.textAlign(p.CENTER, p.CENTER);
            p.textSize(14);
            p.text(node.authorId, node.x, node.y - 15);
            
            p.fill('#a0aec0');
            p.textSize(12);
            const truncatedName = truncateText(node.authorName, 12);
            p.text(truncatedName, node.x, node.y + 5);
            
            p.fill('#68d391');
            p.text(`${node.paperCount} makale`, node.x, node.y + 20);
            
            drawTree(node.left);
            drawTree(node.right);
            }
        };

        function showNotification(authorId) {
            const notification = document.createElement('div');
            notification.textContent = `Yazar ID kopyalandı: ${authorId}`;
            notification.style.position = 'fixed';
            notification.style.bottom = '20px';
            notification.style.right = '20px';
            notification.style.padding = '10px 20px';
            notification.style.backgroundColor = '#4299e1';
            notification.style.color = 'white';
            notification.style.borderRadius = '5px';
            notification.style.zIndex = '1000';
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 2000);
        }

        function copyToClipboard(text) {
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
        }

        function truncateText(text, maxLength) {
            if (!text) return '';
            if (text.length <= maxLength) return text;
            return text.slice(0, maxLength - 2) + '..';
        }

        function calculateAllShortestPaths(authorId) {

            const outputContainer = document.getElementById('outputContainer');
            const startNode = nodes.get(authorId);
            
            if (!startNode) {
                outputContainer.innerHTML = "Yazar bulunamadı!";
                return;
            }

            let distances = {};
            let previous = {};
            let unvisited = new Set();
            let pathSteps = [];

            nodes.get().forEach(node => {
                distances[node.id] = node.id === authorId ? 0 : Infinity;
                previous[node.id] = null;
                unvisited.add(node.id);
            });

            while (unvisited.size > 0) {
                let minDistance = Infinity;
                let currentNode = null;
                
                unvisited.forEach(nodeId => {
                    if (distances[nodeId] < minDistance) {
                        minDistance = distances[nodeId];
                        currentNode = nodeId;
                    }
                });

                if (currentNode === null || distances[currentNode] === Infinity) break;

                pathSteps.push({
                    node: nodes.get(currentNode).label,
                    distance: distances[currentNode],
                    tableState: {...distances}
                });

                unvisited.delete(currentNode);

                edges.get().forEach(edge => {
                    if (edge.from === currentNode || edge.to === currentNode) {
                        const neighbor = edge.from === currentNode ? edge.to : edge.from;
                        if (unvisited.has(neighbor)) {
                            const weight = parseInt(edge.title.match(/İşbirliği Sayısı: (\d+)/)[1]);
                            const newDistance = distances[currentNode] + weight;
                            
                            if (newDistance < distances[neighbor]) {
                                distances[neighbor] = newDistance;
                                previous[neighbor] = currentNode;
                            }
                        }
                    }
                });
            }

            const tableStyles = `
                <style>
                    .path-table {
                        border-collapse: collapse;
                        width: 100%;
                        margin: 15px 0;
                        background-color: #1a1a1a;
                        box-shadow: 0 1px 3px rgba(255,255,255,0.1);
                    }
                    .path-table th {
                        background-color: #4a90e2;
                        color: white;
                        padding: 12px;
                        text-align: left;
                        font-weight: bold;
                        border: 1px solid #357abd;
                    }
                    .path-table td {
                        padding: 10px;
                        border: 1px solid #333;
                        color: #fff;
                    }
                    .path-table tr:nth-child(even) {
                        background-color: #262626;
                    }
                    .path-table tr:hover {
                        background-color: #333333;
                    }
                    .step-header {
                        background-color: #262626;
                        padding: 10px;
                        margin: 10px 0;
                        border-left: 4px solid #4a90e2;
                        font-weight: bold;
                        color: #fff;
                    }
                    .current-node {
                        background-color: #1e3a5f !important;
                        font-weight: bold;
                        color: #fff;
                    }
                    .unreachable {
                        color: #ff4d4d;
                        font-style: italic;
                    }
                </style>
            `;

            const toggleButton = `
                <button id="toggleSizeBtn" style="
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    padding: 5px 10px;
                    background: #4299e1;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    z-index: 1000;
                    font-size: 16px;
                    width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;">⤢</button>
            `;

            outputContainer.innerHTML = `
                ${tableStyles}
                ${toggleButton}
                <h3 style="color: #2c3e50; margin-bottom: 20px;">En Kısa Yol Analizi</h3>
                <p style="font-size: 16px; margin-bottom: 15px;"><strong>Başlangıç Yazarı:</strong> ${startNode.label}</p>
                <div id="pathStepsContainer"></div>
                <div id="finalResults"></div>
            `;

            document.getElementById('toggleSizeBtn').onclick = () => {
                isExpanded = !isExpanded;
                const toggleButton = document.getElementById('toggleSizeBtn');
                
                if (isExpanded) {
                    if (!originalStyles.width) {
                        originalStyles = {
                            width: outputContainer.style.width,
                            height: outputContainer.style.height,
                            overflow: outputContainer.style.overflow,
                            transition: outputContainer.style.transition
                        };
                    }
                    
                    outputContainer.style.width = '1500px';
                    outputContainer.style.height = '800px';
                    outputContainer.style.overflow = 'auto';
                    outputContainer.style.transition = 'all 0.3s ease';
                    toggleButton.style.background = '#e53e3e';
                    toggleButton.innerHTML = '⤡';
                } else {
                    outputContainer.style.width = originalStyles.width;
                    outputContainer.style.height = originalStyles.height;
                    outputContainer.style.overflow = originalStyles.overflow;
                    outputContainer.style.transition = originalStyles.transition;
                    toggleButton.style.background = '#4299e1';
                    toggleButton.innerHTML = '⤢';
                }
            };

            const stepsContainer = document.getElementById('pathStepsContainer');
            pathSteps.forEach((step, index) => {
                setTimeout(() => {
                    let tableHTML = '<table class="path-table">';
                    tableHTML += '<tr><th>Yazar</th><th>Mesafe</th></tr>';
                    
                    Object.keys(step.tableState).forEach(nodeId => {
                        const nodeName = nodes.get(nodeId).label;
                        const distance = step.tableState[nodeId] === Infinity ? "Hesaplanıyor..." : step.tableState[nodeId];
                        const isCurrentNode = nodes.get(nodeId).label === step.node;
                        
                        tableHTML += `
                            <tr class="${isCurrentNode ? 'current-node' : ''}">
                                <td>${nodeName}</td>
                                <td>${"Hesaplanıyor..."}</td>
                            </tr>
                        `;
                    });
                    
                    tableHTML += '</table>';
                    
                    stepsContainer.innerHTML = `
                        <div class="step-header">
                            Adım ${index + 1}: ${step.node} düğümü işleniyor (Mesafe: ${step.distance})
                        </div>
                        ${tableHTML}
                    `;
                }, 1 * index);
            });

            setTimeout(() => {
                let finalHTML = '<h4 style="color: #2c3e50; margin: 20px 0;">Son Durum:</h4>';
                finalHTML += '<table class="path-table">';
                finalHTML += '<tr><th>Yazar</th><th>En Kısa Mesafe</th><th>Yol</th></tr>';

                nodes.get().forEach(node => {
                    if (node.id !== authorId) {
                        let path = [];
                        let current = node.id;
                        
                        while (current !== null) {
                            path.unshift(nodes.get(current).label);
                            current = previous[current];
                        }

                        const isUnreachable = distances[node.id] === Infinity;
                        const distance = isUnreachable ? "Ulaşılamaz" : distances[node.id];
                        const pathStr = path.length > 0 ? path.join(' -> ') : "Yol yok";
                        
                        finalHTML += `
                            <tr class="${isUnreachable ? 'unreachable' : ''}">
                                <td>${node.label}</td>
                                <td>${distance}</td>
                                <td>${pathStr}</td>
                            </tr>
                        `;
                    }
                });
                
                finalHTML += '</table>';
                document.getElementById('finalResults').innerHTML = finalHTML;
            }, 1 * pathSteps.length);

            closeSearchBox();
        }

                function analyzeCollaborations(authorId) {
            const outputContainer = document.getElementById('outputContainer');
            let collaboratorCount = 0;
            let collaboratorNames = [];
            
            edges.get().forEach(edge => {
                if (edge.from === authorId) {
                    collaboratorCount++;
                    let collaborator = nodes.get(edge.to);
                    collaboratorNames.push(collaborator.label);
                } else if (edge.to === authorId) {
                    collaboratorCount++;
                    let collaborator = nodes.get(edge.from);
                    collaboratorNames.push(collaborator.label);
                }
            });

            const authorNode = nodes.get(authorId);
            const authorName = authorNode ? authorNode.label : "Unknown Author";

            outputContainer.innerHTML = `
                <h3>İşbirliği Analizi</h3>
                <p><strong>Yazar:</strong> ${authorName}</p>
                <p><strong>Yazar Orcid:</strong> ${authorId}</p>
                <p><strong>Toplam İşbirliği Sayısı:</strong> ${collaboratorCount}</p>
                <p><strong>İşbirlikçi İsimleri:</strong></p>
                <ul>
                    ${collaboratorNames.map(name => `<li>${name}</li>`).join('')}
                </ul>
            `;
        }

        function bfs(startId) {
            let longestPath = [];
            let queue = [[startId]];

            while (queue.length > 0) {
                let currentPath = queue.shift();
                let lastNode = currentPath[currentPath.length - 1];

                if (currentPath.length > longestPath.length) {
                    longestPath = currentPath;
                }

                edges.get().forEach(edge => {
                    let neighborId = null;
                    if (edge.from === lastNode && !currentPath.includes(edge.to)) {
                        neighborId = edge.to;
                    } else if (edge.to === lastNode && !currentPath.includes(edge.from)) {
                        neighborId = edge.from;
                    }

                    if (neighborId !== null) {
                        queue.push([...currentPath, neighborId]);
                    }
                });
            }

            return longestPath;
        }

        function findLongestPath(startId) {
            const outputContainer = document.getElementById('outputContainer');
            const startNode = nodes.get(startId);
            
            if (!startNode) {
                outputContainer.innerHTML = "Yazar Orcid'i bulunamadı!";
                return;
            }

            let longestPath = bfs(startId);
            let pathNodes = longestPath.map(id => nodes.get(id).label);

            outputContainer.innerHTML = `
                <h3>En Uzun Yol Analizi</h3>
                <p><strong>Başlangıç Yazarı:</strong> ${startNode.label}</p>
                <p><strong>En Uzun Yol Uzunluğu:</strong> ${longestPath.length} düğüm</p>
                <p><strong>Yol:</strong></p>
                <p>${pathNodes.join(' -> ')}</p>
            `;

            highlightLongestPath(longestPath);
        }

        function highlightLongestPath(path) {
            const originalEdgeStyles = edges.get().map(edge => ({id: edge.id,color: edge.color,width: edge.width}));

            edges.get().forEach(edge => {
                edges.update({id: edge.id, color: {color: '#ffffff', opacity: 0.5}});
            });

            let highlightedEdgeIds = [];
            for (let i = 0; i < path.length - 1; i++) {
                edges.get().forEach(edge => {
                    if ((edge.from === path[i] && edge.to === path[i + 1]) ||
                        (edge.from === path[i + 1] && edge.to === path[i])) {
                        edges.update({
                            id: edge.id,
                            color: {color: '#e900ff', highlight: '#ff00ff', opacity: 1},
                            width: 3
                        });
                        highlightedEdgeIds.push(edge.id);
                    }
                });
            }

            setTimeout(() => {
                originalEdgeStyles.forEach(style => {
                    edges.update({
                        id: style.id,
                        color: style.color,
                        width: style.width
                    });
                });
            }, 30000);
        }

        function setoriginal(){
            outputContainer.style.width = originalStyles.width;
            outputContainer.style.height = originalStyles.height;
            outputContainer.style.overflow = originalStyles.overflow;
            outputContainer.style.transition = originalStyles.transition;
        }

        function showOutput(buttonId, context ='') {
            var outputContainer = document.getElementById('outputContainer');
            switch(buttonId) {
                case 1:
                    setoriginal();
                    bstRoot = null;
                    showSearchBox(context);
                    break;
                case 2:
                    setoriginal();
                    showSearchBox(context);
                    break;
                case 3:
                    setoriginal();
                    if (authorQueue.length === 0) {
                        outputContainer.innerHTML = "Uyarı: Önce 1. İsteri Çalıştırarak Kuyruk Oluşturmalısınız!";
                        return;
                    }

                    outputContainer.innerHTML = `
                        <div>
                            <input type="text" id="bstAuthorId" placeholder="Çıkarılacak Yazar ID">
                            <button onclick="processBSTOperation()">İşlemi Gerçekleştir</button>
                        </div>
                    `;
                    if (!bstRoot) {             
                        createBSTFromQueue();
                    }
                    displayBST();
                    break;
                case 4:
                    setoriginal();
                    showSearchBox('case4');
                    break;
                case 5:
                    setoriginal();
                    showSearchBox(context);
                    break;
                case 6:
                    setoriginal();
                    let collaborationCounts = {};
                    edges.get().forEach(edge => {
                        if (!collaborationCounts[edge.from]) {
                            collaborationCounts[edge.from] = 0;
                        }
                        collaborationCounts[edge.from]++;
                        
                        if (!collaborationCounts[edge.to]) {
                            collaborationCounts[edge.to] = 0;
                        }
                        collaborationCounts[edge.to]++;
                    });

                    let maxCollaborations = 0;
                    let mostCollaborativeAuthor = '';
                    for (let authorId in collaborationCounts) {
                        if (collaborationCounts[authorId] > maxCollaborations) {
                            maxCollaborations = collaborationCounts[authorId];
                            mostCollaborativeAuthor = authorId;
                        }
                    }

                    let authorNode = nodes.get(mostCollaborativeAuthor);
                    let authorName = authorNode.label;

                    outputContainer.innerHTML = `En çok işbirliği yapan yazar: ${authorName}<br>
                                            Yazar ID: ${mostCollaborativeAuthor}<br>
                                            İşbirliği sayısı: ${maxCollaborations}`;
                    break;
                case 7:
                    showSearchBox('case7');
                    break;
                default:
                    outputContainer.innerHTML = "Çıktı Burada Gözükecek...";
                }
            }
        </script>
    """
    html = html.replace("<body>", "<body>" + body_html_content)

    additional_script = """
        window.nodes = new vis.DataSet(""" + str([{
            'id': node.id,
            'label': node.name,
            'authored_papers': node.authored_papers,
        } for node in nodes.values()]) + """);

        network.on('selectNode', function (params) {
            var selectedNodeId = params.nodes[0];
            var selectedNode = nodes.get(selectedNodeId);
            var outputContainer = document.getElementById('outputContainer');
            setoriginal();
            
            var authoredPapersHtml = selectedNode.authored_papers.length > 0 
                ? '<div class="paper-section"><h4>Yazarın Yazdığı Makaleler:</h4><ul>' +
                  selectedNode.authored_papers.map((paper, index) => 
                    `<li>${index + 1}. ${paper}</li>`).join('') + '</ul></div>'
                : '';

            outputContainer.innerHTML = `
                <div class="author-info">
                    <h3>${selectedNode.label}</h3>
                    <p><strong>Yazar Orcid:</strong> ${selectedNodeId}</p>
                    ${authoredPapersHtml}
                </div>
            `;
        });
    """

    html = html.replace("network = new vis.Network(container, data, options);", "network = new vis.Network(container, data, options);" + additional_script)

    with open("proje3.html", "w", encoding="utf-8") as f:
        f.write(html)

visualize_network()