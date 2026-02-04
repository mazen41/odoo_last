# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

# TASK 2.1 – Quotation Stages Model
class EngineeringQuotationStage(models.Model):
    _name = 'engineering.quotation.stage'
    _description = 'Engineering Quotation Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(default=10)
    
    # حقل المرحلة التالية (يربط المرحلة الحالية بالمرحلة التي تليها)
    next_stage_id = fields.Many2one('engineering.quotation.stage', string="Next Stage")
    
    # اسم الزر الذي سيظهر في هذه المرحلة
    button_name = fields.Char(string="Button Label", help="The text that will appear on the button to move to the Next Stage.")
    
    is_approved_stage = fields.Boolean(string="Is Approved Stage?")
    is_rejected_stage = fields.Boolean(string="Is Rejected Stage?")

# TASK 2.2 – Stage History Tracking
class EngineeringQuotationStageHistory(models.Model):
    _name = 'engineering.quotation.stage.history'
    _description = 'Quotation Stage History'
    _order = 'change_date desc'

    quotation_id = fields.Many2one('sale.order', string='Quotation', ondelete='cascade')
    from_stage_id = fields.Many2one('engineering.quotation.stage', string='From Stage')
    to_stage_id = fields.Many2one('engineering.quotation.stage', string='To Stage')
    changed_by_id = fields.Many2one('res.users', string='Changed By', default=lambda self: self.env.user)
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)

# TASK 2.3 – Extend Sale Order
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quotation_stage_id = fields.Many2one(
        'engineering.quotation.stage',
        string='Quotation Stage',
        tracking=True,
        default=lambda self: self.env['engineering.quotation.stage'].search([], order='sequence', limit=1)
    )
    stage_history_ids = fields.One2many(
        'engineering.quotation.stage.history',
        'quotation_id',
        string='Stage History'
    )

    # هذا هو أهم جزء: تعديل منطق زر التأكيد
    # TASK 2.6 – Confirm Quotation Override (CRITICAL)
    def action_confirm(self):
        # 1. استدعاء المنطق الأصلي في Odoo أولاً (لإنشاء أمر البيع وتثبيت السعر)
        res = super(SaleOrder, self).action_confirm()

        # 2. البحث عن مرحلة "Approved"
        approved_stage = self.env['engineering.quotation.stage'].search([('is_approved_stage', '=', True)], limit=1)
        if not approved_stage:
            # في حال لم يجدها، يمكن إنشاءها أو إظهار خطأ
            # For simplicity, we will assume it exists from the data file.
            pass

        for order in self:
            # 3. تسجيل الحركة في سجل التتبع
            self.env['engineering.quotation.stage.history'].create({
                'quotation_id': order.id,
                'from_stage_id': order.quotation_stage_id.id,
                'to_stage_id': approved_stage.id,
            })
            
            # 4. تغيير مرحلة عرض السعر إلى "Approved"
            order.write({'quotation_stage_id': approved_stage.id})

            # 5. إنشاء الفاتورة تلقائيًا (يمكن تعديل المنطق لاحقًا)
            order._create_invoices()
            
            # 6. إنشاء المشروع تلقائيًا
            project = order._create_engineering_project()
            
            # 7. ربط المشروع بعرض السعر
            order.write({'project_id': project.id})

        # 8. (اختياري لكن مهم) إعادة توجيه المستخدم إلى المشروع الجديد
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': self.project_id.id,
            'view_mode': 'form',
            'views': [(self.env.ref('project.edit_project').id, 'form')],
            'target': 'current',
        }

    def _create_engineering_project(self):
        self.ensure_one()
        # 5️⃣ تحويل البيع إلى مشروع حقيقي
        project = self.env['project.project'].create({
            'name': f"{self.name} - {self.partner_id.name}",
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id,
            # يمكنك إضافة حقول أخرى هنا
        })

        # 6️⃣ تجهيز طريق المشروع (Project Roadmap)
        stages = [
            'التصميم المبدئي (الكروكي)', 'التعاقد وجمع الوثائق', 'الموافقات الخارجية',
            'التصميمات التفصيلية', 'الإشراف الهندسي', 'إنهاء المشروع'
        ]
        
        project_stage_model = self.env['project.task.type']
        for index, stage_name in enumerate(stages):
            project_stage_model.create({
                'name': stage_name,
                'project_ids': [(4, project.id)],
                'sequence': index + 1,
            })
        
        # 8️⃣ فتح شغل فعلي للموظفين (مثال مبسط)
        # 7️⃣ وضع المشروع في أول خطوة
        first_stage = project_stage_model.search([('project_ids', 'in', project.id)], order='sequence', limit=1)
        if first_stage:
            self.env['project.task'].create({
                'name': 'إعداد الكروكي المبدئي للمشروع',
                'project_id': project.id,
                'stage_id': first_stage.id,
                # يمكنك تحديد مسؤول المهمة هنا
            })
        
        return project
    
    def action_move_to_next_stage(self):
        self.ensure_one()
        current_stage = self.quotation_stage_id
        next_stage = current_stage.next_stage_id
        
        if next_stage:
            # 1. تسجيل الحركة في سجل التتبع
            self.env['engineering.quotation.stage.history'].create({
                'quotation_id': self.id,
                'from_stage_id': current_stage.id,
                'to_stage_id': next_stage.id,
            })
            
            # 2. نقل الـ Quotation إلى المرحلة التالية
            self.write({'quotation_stage_id': next_stage.id})

            # 3. (اختياري) إنشاء Task داخلي:
            if next_stage.name == 'تسعير ومراجعة':
                self.env['project.task'].create({
                    'name': _('Review Pricing for Quotation: %s', self.name),
                    'project_id': self.project_id.id, # ربط المهمة بمشروع إذا كان موجوداً
                    'user_id': self.env.user.id, # تعيين المهمة للمستخدم الحالي
                })

            # إعادة تحميل الصفحة
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        else:
            return {
                'warning': {
                    'title': _("No Next Stage"),
                    'message': _("There is no defined next stage for the current stage: %s.", current_stage.name),
                }
            }

    # دالة مساعدة لتحديد ما إذا كان يجب إظهار الزر
    @api.depends('quotation_stage_id')
    def _compute_next_stage_button_name(self):
        for order in self:
            if order.quotation_stage_id and order.quotation_stage_id.next_stage_id and not order.state in ('sale', 'done', 'cancel'):
                order.next_stage_button_name = order.quotation_stage_id.button_name
                order.show_next_stage_button = True
            else:
                order.next_stage_button_name = False
                order.show_next_stage_button = False

    next_stage_button_name = fields.Char(compute='_compute_next_stage_button_name')
    show_next_stage_button = fields.Boolean(compute='_compute_next_stage_button_name')

    def action_create_and_send_contract(self):
        self.ensure_one()
        
        # 1. البحث عن مرحلة "التعاقد"
        contract_stage = self.env['engineering.quotation.stage'].search([('name', '=', 'التعاقد وجمع الوثائق')], limit=1)
        
        # 2. التأكد من أن عرض السعر في مرحلة "التعاقد"
        if self.quotation_stage_id.name != 'التعاقد وجمع الوثائق':
            raise UserError(_("This action is only allowed when the Quotation is in the 'Contracting & Documents Collection' stage."))
        
        # 3. إنشاء مستند مشروع جديد وفتح شاشته (بدلاً من الإرسال المباشر)
        new_doc = self.env['engineering.project.document'].create({
            'name': _("Contract for Quotation: %s" % self.name),
            'quotation_id': self.id,
            'project_id': self.project_id.id,
        })
        
        # 4. فتح شاشة المستند الجديد ليقوم المستخدم برفع الملف وإرساله
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'engineering.project.document',
            'res_id': new_doc.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': self.env.context,
        }
    def action_send_quotation_whatsapp(self):
        self.ensure_one()
        customer_phone = self.partner_id.phone
        
        if not customer_phone:
            raise UserError(_("Customer phone number is missing. Please add it to the contact card."))

        cleaned_phone = ''.join(filter(str.isdigit, customer_phone))
        
        # رابط عرض السعر الذي تم إنشاؤه مسبقًا في Odoo (مهم للإرفاق)
        report_url = self.get_portal_url() if self.state in ('sent', 'sale') else ""
        
        # يمكن إضافة رابط PDF مباشرة في رسالة الواتساب إذا كان متاحًا
        message = _("Please review the attached quotation: %s" % self.name)
        
        # إذا كان عرض السعر قد أرسل وتم توليد الرابط، أضف الرابط.
        if report_url:
            message += f" {report_url}"

        # بناء رابط WhatsApp
        whatsapp_url = "https://web.whatsapp.com/send?phone=%s&text=%s" % (
            cleaned_phone, 
            message.replace(' ', '%20') # ترميز المسافات
        )
        
        # يمكنك هنا إضافة تحديث لمرحلة عرض السعر إلى "مرسل للعميل" تلقائياً
        if self.quotation_stage_id.name != 'مرسل للعميل':
            sent_stage = self.env['engineering.quotation.stage'].search([('name', '=', 'مرسل للعميل')], limit=1)
            if sent_stage:
                 self.write({'quotation_stage_id': sent_stage.id})
                 # تسجيل الحركة في سجل التتبع
                 self.env['engineering.quotation.stage.history'].create({
                    'quotation_id': self.id,
                    'from_stage_id': self.quotation_stage_id.id,
                    'to_stage_id': sent_stage.id,
                })


        # إعادة توجيه المستخدم
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new', 
        }