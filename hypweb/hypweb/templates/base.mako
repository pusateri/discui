<!DOCTYPE html>

<%!
    nav_sections = (
        ("Summary", "summary"),
        ("Interfaces", "interfaces"),
        ("Queries", "queries"),
        ("DNS", "browse_domains"),
	("Debug", "debug"),
        )
%>


<html>
<head>
    <meta charset="utf-8">
    <title>${self.title()}</title>
    <link rel="stylesheet" href="${request.static_url('hypweb:static/style/jquery-ui-1.10.3.overcast.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('hypweb:static/style/reset.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('hypweb:static/style/hyp.css')}" type="text/css" media="screen" charset="utf-8" />
    <script src="${request.static_url('hypweb:static/scripts/jquery-2.0.3.min.js')}" type="text/javascript"></script>
    ${self.head_extra()}
</head>
<body>
    <div id="search">
        
    </div>
    <div id="hd">
        <div class="cmdbar">
            % if login:
                ${login} |
		<a href="${request.route_url('signout')}">Logout</a> |
               	<a href="${request.route_url('profile')}">Profile</a> |
		<a href="${request.route_url('feedback')}">Feedback</a> |
            % endif
	    <a href="#">Help</a> |
	    <a href="#">About</a>
        </div>

	<h1 class="ui-widget"><a href="${request.route_url('home')}">DNS Hyp (DNS-SD Hybrid Proxy)</a></h1>

        <div id="navbar2" class="ui-tabs ui-widget ui-widget-content ui-corner-all">
            <ul class="ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all">
                % for label, name in nav_sections:
                % if name == capture(self.nav_section):
		<li class="ui-state-default ui-corner-top ui-tabs-selected ui-state-active"><a href="${request.route_url(name)}">${label}</a></li>
                % elif name:
		<li class="ui-state-default ui-corner-top"><a href="${request.route_url(name)}">${label}</a></li>
                % else:
                <li>${label}</li>
                % endif
                % endfor
            </ul>
        </div>

        <% messages = request.session.pop_flash() %>
        % if messages:
        <ul id="flash-messages">
          % for message in messages:
          <li>${message}</li>
          % endfor
        </ul>
        % endif
    </div>

    <div id="bd">
        ${self.wrapbody()}
    </div>

    <div id="ft">
        ${self.footer()}
    </div>
</body>
</html>

<%def name="wrapbody()">
    <div id="main">
        ${next.body()}
    </div>
</%def>

<%def name="head_extra()"></%def>
<%def name="title()">DNS Hyp</%def>
<%def name="nav_section()"></%def>
<%def name="footer()">Copyright 2013-2014 bangj, LLC.</%def>

