class ProjectProject(models.Model):
    _inherit = 'project.project'

    # --- Existing Fields (Keep these as they are) ---
    sale_order_id = fields.Many2one('sale.order', string='Source Quotation', readonly=True)
    
    # --- FILLED IN THE SELECTION OPTIONS HERE ---
    building_type = fields.Selection([
        ('residential', 'سكن خاص'), 
        ('investment', 'استثماري'), 
        ('commercial', 'تجاري'), 
        ('industrial', 'صناعي'), 
        ('cooperative', 'جمعيات وتعاونيات'), 
        ('mosque', 'مساجد'), 
        ('hangar', 'مخازن / شبرات'), 
        ('farm', 'مزارع')
    ], string="نوع المبنى")

    service_type = fields.Selection([
        ('new_construction', 'بناء جديد'), 
        ('demolition', 'هدم'), 
        ('modification', 'تعديل'), 
        ('addition', 'اضافة'), 
        ('addition_modification', 'تعديل واضافة'), 
        ('supervision_only', 'إشراف هندسي فقط'), 
        ('renovation', 'ترميم'), 
        ('internal_partitions', 'قواطع داخلية'), 
        ('shades_garden', 'مظلات / حدائق')
    ], string="نوع الخدمة")
    
    region = fields.Char(string="المنطقة (Region)")
    plot_no = fields.Char(string="رقم القسيمة")
    block_no = fields.Char(string="القطعة")
    street_no = fields.Char(string="الشارع")
    area = fields.Char(string="المساحة (Area)")

    # --- NEW FIELDS (From your paper form) ---
    floor_basement = fields.Text(string="أولاً السرداب")
    floor_ground = fields.Text(string="ثانياً الدور الأرضي")
    floor_first = fields.Text(string="الدور الأول")
    floor_second = fields.Text(string="الدور الثاني")
    floor_roof = fields.Text(string="الدور السطح")

    # --- NEW FUNCTION (For the WhatsApp button) ---
    def action_send_project_form_whatsapp(self):
        self.ensure_one()
        phone = self.partner_id.mobile or self.partner_id.phone
        if not phone:
            raise UserError("رقم الهاتف مفقود للعميل")
        
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        # We must generate a secure access token for the portal link to work
        self._portal_ensure_token()
        project_url = f"{base_url}{self.get_portal_url()}"
        
        message = _("مرحباً %s،\nنرفق لكم نموذج تفاصيل المشروع الخاص بكم:\n%s") % (self.partner_id.name, project_url)
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://web.whatsapp.com/send?phone={cleaned_phone}&text={encoded_message}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }
