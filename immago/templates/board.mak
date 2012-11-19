<%inherit file="base.html"/>

<%include file="post_form.html"/>

% for thread in latest_threads:
	<a href="${request.route_path('thread', thread_id=thread.id)}">Reply</a>
	% for post in thread.posts:
		${post.msg} <br />
	% endfor
% endfor

