<!DOCTYPE html>

<html>
<head>
    <meta charset="utf-8">
    <title>DNS Hyp</title>
    <link rel="stylesheet" href="${request.static_url('hypweb:static/style/reset.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('hypweb:static/style/hyp.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('hypweb:static/style/home.css')}" type="text/css" media="screen" charset="utf-8" />
</head>
<body>

<div id="bg">
	<div id="sign-in">
	    ${form.begin(request.route_url('login')) }
	    ${form.csrf_token() }
	    <div>
	        ${form.errorlist("email") }
	        ${form.label("Email") }
	        ${form.text('email') }
	    </div>
	    <div>
	        ${form.errorlist("password") }
	        ${form.label("Password") }
	        ${form.password('password') }
	    </div> 
	    ${form.submit("submit", "Sign in") }
	    ${form.end() }
	</div>
    <div>
        <% messages = request.session.pop_flash() %>
        % if messages:
        <ul id="flash-messages">
          % for message in messages:
          <li>${message}</li>
          % endfor
        </ul>
        % endif
    </div> 
    <div>
    	<h1 class="tagline">DNS <span>Hy</span>p</h1>
		<h2 class="subtagline">DNS Service Discovery Hybrid Proxy</h2>
	    <div class="feature">
		<h3>Portable</h3>
		<p>Runs on most BSD and Linux operating systems.</p>
	    </div>
	    <div class="feature">
		<h3>Scalable</h3>
		<p>Supports configurable policy across many interfaces.</p>
	    </div>
	    <div class="feature">
		<h3>Configureable</h3>
		<p>You decide which services get advertised on which networks.</p>
	    </div>
	    <div class="feature">
		<h3>Extensible</h3>
		<p>Use the RESTful API to talk to hypd for configuration.</p>
	    </div>
	    <div class="feature">
		<h3>Secure</h3>
		<p>Provision interfaces into separate customer instances.</p>
	    </div>
	</div>
</div>

</body>
</html>
