//import PREPRINT_DATA from "./data-preprint.js";
//import PAPERS_DATA from "./data-papers.js";


function LienSpecial(nom) {
   const liensLogos = [
      { "nom": "arxiv", "src": "img/arxiv-logo.svg" },
      { "nom": "PDF", "src": "img/pdf-logo.svg" },
      { "nom": "Code", "src": "img/code-logo.svg" },
   ];
   
   for (const logo of liensLogos) {
      if (nom.toLowerCase().trim() === logo.nom.toLowerCase().trim()) {
         const img = document.createElement("img");
         img.alt = logo.nom;
         img.src = logo.src;
         img.style.height = "1lh";
         img.style.display = "inline-block";
         img.title = logo.nom;
         
         return img;
      }
   }
   
   return null;
}

function GenererLiens(liens) {
   const div = document.createElement("div");
   for (const lien in liens) {
      const a = document.createElement("a");
      
      a.className = "research-lien";
      a.href = liens[lien];
      a.target = "_blank";
      
      /*let contenu = null;*/
      let contenu = LienSpecial(lien);
      if (contenu === null) {
         a.textContent = lien;
      } else {
         a.appendChild(contenu);
      }
      
      div.appendChild(a);
   }
   
   return div;
}

function ChargerDonnees(id, articles) {
   const elem = document.getElementById(id);
   
   if (elem) {
      for (const article of articles) {
         const li = document.createElement("li");
         let span;
         
         span = document.createElement("span");
         span.className = "research-titre";
         span.textContent = article.titre;
         li.appendChild(span);
         
         span = document.createElement("span");
         span.className = "research-auteurs";
         span.textContent = article.auteurs;
         li.appendChild(span);
         
         let time = document.createElement("time");
         time.className = "research-annee";
         time.textContent = " (" + article.annee + ")";
         time.dateTime = article.annee;
         li.appendChild(time);

         span = document.createElement("span");
         span.className = "research-acceptedat";
         span.textContent = article.acceptedat;
         li.appendChild(span);
         
         li.appendChild(GenererLiens(article.liens));
         
         elem.appendChild(li);
      }
   }
}




window.addEventListener("load", () => {
   ChargerDonnees("preprint", PREPRINT_DATA);
   ChargerDonnees("papers", PAPERS_DATA);
});
