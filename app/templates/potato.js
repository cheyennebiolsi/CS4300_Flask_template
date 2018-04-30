<script type="text/javascript"> 
	var typeHeadEngine = new Bloodhound({ 
		limit: 10, 
		remote: { url: 'Services/WebServiceAjax.asmx/GetProjID', 
			ajax: { 
				type: "POST", 
				data: '{}', 
				cache: false, 
				contentType: "application/json; charset=utf-8", 
				dataType: "text" }, 
			filter: function (data) { 
				var obj = JSON.parse(data); console.log(obj.d); return obj.d; 
			} 
		}, 
		limit:25, 
		datumTokenizer: function (d) { 
			return Bloodhound.tokenizers.whitespace(value); 
		}, 
		queryTokenizer: Bloodhound.tokenizers.whitespace 
	}); // kicks off the loading/processing of `local` and `prefetch` 
	typeHeadEngine.initialize(); // passing in `null` for the `options` arguments will result in the default 
	// options being used 
	$('#scrollable-dropdown-menu .typeahead').typeahead(null, { 
		name: 'Name', 
		displayKey: 'Value', 
		//highlight: true, 
		//hint: true, 
		// `ttAdapter` wraps the suggestion engine in an adapter that 
		// is compatible with the typeahead jQuery plugin source: typeHeadEngine.ttAdapter() }); Here is the ASP.NET CODE _ Public Function GetProjID() As List(Of ListItem) ``` Dim query As String = "SELECT DISTINCT PROJ_DESCR FROM INL_Reporting.labor.Projects WHERE INT_LAB_RATE_TYPE <> 'NONE' AND ACTIVE = 1 ORDER BY PROJ_DESCR" Dim constr As String = ConfigurationManager.ConnectionStrings("Connection_String").ConnectionString Dim fruits As New List(Of ListItem)() Using con As New SqlConnection(constr) Using cmd As New SqlCommand(query) Using sda As New SqlDataAdapter() cmd.Connection = con sda.SelectCommand = cmd Using dt As New DataTable() con.Open() Using sdr As SqlDataReader = cmd.ExecuteReader() While sdr.Read() fruits.Add(New ListItem() With { _ .Text = sdr("PROJ_DESCR").ToString(), _ .Value = sdr("PROJ_DESCR").ToString() _ }) End While End Using End Using End Using End Using End Using Return fruits End Function ``` 