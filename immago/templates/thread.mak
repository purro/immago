<%inherit file="base.html"/>
<%include file="post_form.html" args="thread_id=thread.id"/>

% for post in thread.posts:
	${post.msg}<br />
% endfor
