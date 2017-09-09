"use strict";

let figures = document.getElementsByTagName("figure");
let codeCount = 0, figureCount = 0, outputCount = 0;

for (let i = 0; i < figures.length; ++i) {
	// simple name
	let figure = figures[i];

	// get content tag
	let figContent =
	    figure.getElementsByTagName('img')[0]
	||  figure.getElementsByTagName('pre')[0]
	||  figure.getElementsByTagName('output')[0];

	let type = figContent.tagName.toLowerCase();

	// get the count of the type
	let count = -1;
	switch (type) {
		case "figure": count = ++figureCount; break;
		case "output": count = ++outputCount; break;
		case "pre":    count = ++codeCount;   break;
	}

	// get the title (or caption if no title)
	let figTitle =
	    figure.getElementsByTagName('h4')[0]
	||  figure.getElementsByTagName('figcaption')[0];

	// prepend count to title
	figTitle.insertAdjacentHTML("afterbegin", `${count}: `);

	// add count to references
	let references = document.getElementsByClassName(figure.id);
	console.log(references);
	for (let j = 0; j < references.length; ++j) {
		let reference = references[j];

		// get the semantic name for the type
		let typeName = "None"
		switch (type) {
			case "figure": typeName = "figur";           break;
			case "output": typeName = "programutskrift"; break;
			case "pre":    typeName = "programutskrift"; break;
		}
		reference.innerHTML = `${typeName} ${count}`;
		reference.href = `#${figure.id}`;
	}
}
