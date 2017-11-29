<%!
    import config.python
%># production requirements
% for a in config.python.install_requires:
${a}
% endfor
# dev requirements
% for a in config.python.dev_requires:
${a}
% endfor
