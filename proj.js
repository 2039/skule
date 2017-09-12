"use strict";

let questions = document.getElementsByClassName("question");

for (let i = 0; i < questions.length; ++i) {
	let question = questions[i];

	question.style.display = "none"
	let toggleQuestionButton = document.createElement("button");
	toggleQuestionButton.innerHTML = "(toggle question)";
	toggleQuestionButton.classList.add("toggle");
	toggleQuestionButton.onclick = (e) => {
		if (question.style.display === "none")
			{ question.style.display = "block" }
		else
			{ question.style.display = "none" }
	}
	question.after(toggleQuestionButton);
}

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

	// get the tag name
	let type = figContent.tagName.toLowerCase();

	// get the count and the semantic name for the type
	let count = -1;
	let typeName = "None"
	switch (type) {
		case "img": 	 count = ++figureCount; typeName = "figure";  break;
		case "output": count = ++outputCount; typeName = "listing"; break;
		case "pre":    count = ++codeCount;   typeName = "listing"; break;
	}

	// get the title (or caption if no title)
	let figTitle =
	    figure.getElementsByTagName('h4')[0]
	||  figure.getElementsByTagName('figcaption')[0];

	// prepend count to title
	figTitle.insertAdjacentHTML("afterbegin", `${typeName} ${count}: `);

	// add count to references
	let references = document.getElementsByClassName(figure.id);
	for (let j = 0; j < references.length; ++j) {
		let reference = references[j];
		reference.innerHTML = `${typeName} ${count}`;
		reference.href = `#${figure.id}`;
	}
}
