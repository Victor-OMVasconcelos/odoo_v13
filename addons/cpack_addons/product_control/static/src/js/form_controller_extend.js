/** @odoo-module **/
import FormController from 'web.FormController';

FormController.include({

    _onButtonClicked: function (event) {
        const name = event.data.attrs.name;

        if (name === 'add_info' || name == 'add_coil_band') {

            this.trigger_up('save_record', {
                callback: () => {
   
                    this._super(event);
                },
            });
        } else {
 
            this._super(event);
        }
    },
});
