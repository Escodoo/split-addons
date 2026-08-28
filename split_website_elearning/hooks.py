# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def pre_init_hook(env):
    """Reuse xmlids from the former split_elearning technical name."""
    env.cr.execute(
        """
        UPDATE ir_model_data
           SET module = 'split_website_elearning'
         WHERE module = 'split_elearning'
        """
    )
    env.cr.execute(
        """
        UPDATE ir_module_module
           SET state = 'uninstalled'
         WHERE name = 'split_elearning'
        """
    )


def post_init_hook(env):
    env["website"]._split_website_elearning_setup()
