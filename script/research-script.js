//import PAPERS_DATA from "./papers-data.js";
//import PREPRINTS_DATA from "./preprints-data.js";
//import TALKS_DATA from "./talks-data.js";

function LienSpecial(nom) {
   const liensLogos = [
      { "nom": "arxiv", "src": "img/arxiv-logo.svg" },
      { "nom": "PDF", "src": "img/pdf-logo.svg" },
      { "nom": "Code", "src": "img/code-logo.svg" },
      { "nom": "event-page"},
      { "nom": "slides"},

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
   console.log(articles)
   console.log("-------------------")

   if (articles.length > 0) {
      for (const article of articles) {
         const li = document.createElement("li");
         let span;
         
         span = document.createElement("span");
         span.className = "title";
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
         span.innerHTML = article.acceptedat;
         li.appendChild(span);
         
         li.appendChild(GenererLiens(article.liens));
         
         elem.appendChild(li);
      }
   } 
    /* else {
      const message = document.createElement("p");
      message.textContent = "We require more papers !";
      elem.appendChild(message);
   }
   */
}


function LoadTalks(id, talks) {
   const elem = document.getElementById(id);
   console.log(talks)

   if (elem) {
      for (const talk of talks) {
         const li = document.createElement("li");
         li.className = "talks-with-margin";
         let span;

         /* Title */
         span = document.createElement("span");
         span.className = "title";
         span.textContent = talk.title;
         li.appendChild(span);

         /* Event */
         span = document.createElement("span");
         span.className = "event";
         span.textContent = talk.event + " — ";
         li.appendChild(span);

         /* Location */
         span = document.createElement("span");
         span.className = location;
         span.textContent = "(" + talk.location + ", ";
         li.appendChild(span);

         /* Date */
         span = document.createElement("span");
         span.className = "date";
         span.textContent = talk.date  + ") ";
         li.appendChild(span);

         /*li.appendChild(GenererLiens(article.liens));*/

         elem.appendChild(li);
      }
   }
}



window.addEventListener("load", () => {
   ChargerDonnees("papers", PAPERS_DATA);
   ChargerDonnees("preprints", PREPRINTS_DATA);
   LoadTalks("talks", TALKS_DATA)
});
