<%inherit file="base.html"/>
<%include file="post_form.html" args="thread_id=thread.id"/>

% for post in thread.posts:
	<%include file="post_template.html" args="post=post"/>
% endfor
