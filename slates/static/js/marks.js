
var SUBJECT_LIST = ["Tamil", "English", "Maths", "Science", "Social"];

function getMarks(user_id){
	var exam_name = $('#exam-type').val();
    apiCall('/mark/'+user_id, 'get', {"exam_name":exam_name}, displayMarks);
}

function displayMarks(data){

	var ctx = $("#myChart");
	var myChart = new Chart(ctx, {
		type: 'bar',
		data: {
		labels: SUBJECT_LIST,
		datasets: [{
			label: '# of Marks in '+$('#exam-type').val().toUpperCase(),
			data: [data.s1,data.s2,data.s3,data.s4,data.s5],
			backgroundColor: [
				'rgba(255, 99, 132, 0.2)',
				'rgba(54, 162, 235, 0.2)',
				'rgba(255, 206, 86, 0.2)',
				'rgba(75, 192, 192, 0.2)',
				'rgba(153, 102, 255, 0.2)',
				'rgba(255, 159, 64, 0.2)'
			],
			borderColor: [
				'rgba(255,99,132,1)',
				'rgba(54, 162, 235, 1)',
				'rgba(255, 206, 86, 1)',
				'rgba(75, 192, 192, 1)',
				'rgba(153, 102, 255, 1)',
				'rgba(255, 159, 64, 1)'
			],
			borderWidth: 1
		}]
		},
		options: {
			scales: {yAxes: [{ticks: {beginAtZero:true}}]},
			responsive: true
		}
	});
}