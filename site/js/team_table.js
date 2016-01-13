
function json2tables(json_url, div_id, col_config){
	$.getJSON(json_url, function(data) {
		teams = Object.keys(data)
		for (var team_name in data) {
			var team = data[team_name]
  			var tbl_body = ''
			var tbl_head = '<tr>'
			var cols = Object.keys(team[0])
			var fpoints = 0;

			

			$.each(cols, function(i, col){
				tbl_head += '<th>'+col+'</th>'
			})
			tbl_head += '</tr>'

			

			$.each(team, function(){
				var tbl_row = '';
				var row = this;
				row['points'] = parseFloat(row['points']).toFixed(1)
				fpoints += Number(row['points'])
				
				$.each(cols, function(i, col){
					tbl_row += '<td>'+row[col]+'</td>'
				})

				tbl_body += "<tr>"+tbl_row+'</tr>'
			})

			var tbl_title = '<tr><th colspan='+String(cols.length)+'>'+team_name+" "+String(fpoints.toFixed(1))+" Points</th></tr>"
			tbl_head = tbl_title + tbl_head

			//total_row = '<tr><td>Total:</td><td>'+String(fpoints.toFixed(1))+"</td></tr>"
			//tbl_body = total_row + tbl_body
			//console.log(tbl_head)
			//console.log(tbl_body)

			$('<table><thead>'+tbl_head+'</thead><tbody>'+tbl_body+'</tbody></table>').appendTo('#'+div_id)
		}
		
	})
}

json2tables('../teams_2016/current.json', 'tables')
