<%inherit file="base.html"/>

<%include file="post_form.html"/>

% for thread in latest_threads:
	<div class="row">
		<a href="${request.route_path('thread', thread_id=thread.id)}">Reply</a>
		<br/>
		<div class="indent">
			% for post in thread.posts:
				<%include file="post_template.html" args="post=post"/>
			% endfor
		</div>
	</div>
% endfor

