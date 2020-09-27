var load = document.querySelector('#load')
var blog = document.querySelector('#blog')

function b64DecodeUnicode(str) {
    // Going backwards: from bytestream, to percent-encoding, to original string.
    str = str.replace(/[^a-z0-9 ,.?!]/ig, '')
    return(atob(str))
}

function loadPosts() {
	fetch('/load').then((res)=>{
		res.json().then((data) => {

			for(let i = 0; i < data.length; i++) {
				post = `
				<link rel="stylesheet" type="text/css" href="../static/stylesheet.css" />
				<div class = "post" id = "post">
					<h5 id="title">
						${data[i]['title']}
					<div class = "bottomline"></div>
				</h5>
				<hr>`
				for(let content in data[i]['content']) {
					post += `<br>`
					if (content.includes('p')) {
						post += `<p>${data[i]['content'][content]}</p>`
					}
					if(content.includes('img')) {
						img = JSON.stringify(data[i]['content'][content]['$binary']);
						img = img.replace(/[^a-z0-9 ,.?!]/ig, '')
						img = atob(img)
						post += `<img src="data:image; base64, ${img}" alt="image failed" class="post_image"><br>`
					}
				}
				let id = JSON.stringify(data[i]['_id']['$oid']);
				id = id.replace(/[^a-z0-9 ,.?!]/ig, '')
				post += `
					<form action="/readmore/${id}">
						<button class = "readmore" type="submit" value="Read More">Read More</button>
					</form>
				</div>
				<br>`
				blog.innerHTML += post;
			}
		})
	})
}


var interob = new IntersectionObserver(entries => {loadPosts();});

interob.observe(load)