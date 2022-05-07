<%!
    import config.python
%># THIS IS AN AUTO-GENERATED FILE. DO NOT EDIT!
% if hasattr(config.python, "setup_requires"):
# setup requirements
% for a in config.python.setup_requires:
${a}
% endfor
% endif
% if hasattr(config.python, "install_requires"):
# production requirements
% for a in config.python.install_requires:
${a}
% endfor
% endif
% if hasattr(config.python, "dev_requires"):
# dev requirements
% for a in config.python.dev_requires:
${a}
% endfor
% endif
% if hasattr(config.python, "test_requires"):
# test requirements
% for a in config.python.test_requires:
${a}
% endfor
% endif
