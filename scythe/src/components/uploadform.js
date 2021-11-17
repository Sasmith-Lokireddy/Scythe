import React from 'react';

function changeHandler(e) {
	console.log(e.target.files[0].name);
}

function handleSubmission() {

}

export default function UploadForm() {
	return (
		<div>
			<input type="file" name="file" onChange={changeHandler} />
			<div>
				<button onClick={handleSubmission}>Submit</button>
			</div>
		</div>
	);
}
