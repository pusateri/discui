<%inherit file="/base.mako" />

<%def name="head_extra()">
<link rel="stylesheet" href="${request.static_url('hypweb:static/style/ui.jqgrid.css')}" type="text/css" media="screen" charset="utf-8" />
<script src="${request.static_url('hypweb:static/scripts/grid.locale-en.js')}" type="text/javascript"></script>
<script src="${request.static_url('hypweb:static/scripts/jquery.jqGrid.min.js')}" type="text/javascript"></script>
</%def>
<%def name="nav_section()">dns</%def>

	<table id="browse_domains"></table>
	<div id="pager1"></div>
	<table id="domains"></table>
	<div id="pager2"></div>
	<script type="text/javascript">
	$("#browse_domains").jqGrid({
		data: ${browse_domains|n},
		datatype: "local",
		height: 'auto',
	   	colModel:[
			{name:'name',label:'Subdomain', width:250},
                        {name:'ifName',label:'Interface Name', width:150},
                        {name:'ifIndex',label:'Interface Index', width:100},
                        {name:'disabled',label:'Admin Disabled', width:100},
                        {name:'discoveredViaDomainPtr',label:'Domain PTR', width:85},
                        {name:'NSActive',label:'NS Active', width:65},
                        {name:'discoveredViaLBInAddrPtr',label:'Browseable Net RevAddr', width:160},
                        {name:'browseable',label:'Browseable', width:80},
                        {name:'lastRefresh',label:'Last Refreshed (sec)', width:140},
                        {name:'timeout',label:'Times out (sec)', width:100},
	   	],
		pager:"#pager1",
		pgbuttons:false,
		pginput:false,
		sortname: "active",
		sortorder: "desc",
		caption: "Known Browse Domains",
		loadonce:true,
	}).navGrid("#pager1",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for Browse Domain",refresh:false});

	$("#domains").jqGrid({
		data: ${domains|n},
		datatype: "local",
		height: 'auto',
	   	colModel:[
			{name:'name',label:'Name', width:250},
                        {name:'disabled',label:'Admin Disabled', width:100},
                        {name:'lastRefresh',label:'Last Refreshed (sec)', width:150},
                        {name:'timeout',label:'Times out (sec)', width:100},
                        {name:'discoveredViaHostname',label:'Hostname', width:70},
                        {name:'discoveredViaResolvConf',label:'resolv.conf', width:75},
                        {name:'discoveredViaInAddrPtr',label:'Address PTR', width:120},
                        {name:'browseable',label:'Browseable', width:80},
	   	],
		pager:"#pager2",
		pgbuttons:false,
		pginput:false,
		sortname: "active",
		sortorder: "desc",
		caption: "Known Domains",
		loadonce:true,
	}).navGrid("#pager2",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for Domain",refresh:false});
	</script>
