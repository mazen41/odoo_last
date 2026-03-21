# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
import urllib.parse

# ==============================================================================
#  WORKFLOW TEMPLATES (خرائط سير العمل)
# ==============================================================================
WORKFLOW_TEMPLATES = {
    'res_new':[
        {'code': 'rn_1_1', 'name': '1- تصميم الكروكي', 'stage': 'المرحلة الأولى', 'role': 'architect_id'},
        {'code': 'rn_1_2', 'name': '2- تجميع المستندات', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'rn_1_3', 'name': '3- العقد وتحصيل الدفعة الأولى', 'stage': 'المرحلة الأولى', 'role': 'accountant_id'},
        {'code': 'rn_1_4', 'name': '4- تجهيز النماذج والتعهدات والتوقيع', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'rn_1_5', 'name': '5- فحص التربة - كتاب الكهرباء', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'rn_2_1', 'name': '1- سيستم الأعمدة', 'stage': 'المرحلة الثانية', 'role': 'structural_id'},
        {'code': 'rn_2_2', 'name': '2- الواجهات', 'stage': 'المرحلة الثانية', 'role': 'facade_draftsman_id'},
        {'code': 'rn_2_3', 'name': '3- رسم مخطط البلدية', 'stage': 'المرحلة الثانية', 'role': 'muni_draftsman_id'},
        {'code': 'rn_3_1', 'name': '1- إرسال للبلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'rn_3_2', 'name': '2- اعتماد البلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'rn_3_3', 'name': '3- تحصيل الدفعة الأخيرة من العقد', 'stage': 'المرحلة الثالثة', 'role': 'accountant_id'},
        {'code': 'rn_4_1', 'name': '1- تصميم المخطط الإنشائي', 'stage': 'المرحلة الرابعة', 'role': 'structural_id'},
        {'code': 'rn_4_2', 'name': '2- تصميم مخطط الصحي', 'stage': 'المرحلة الرابعة', 'role': 'draftsman_id'},
        {'code': 'rn_4_3', 'name': '3- تصميم مخطط الكهرباء', 'stage': 'المرحلة الرابعة', 'role': 'electrical_id'},
        {'code': 'rn_4_4', 'name': '4- تصميم مخطط الفرش', 'stage': 'المرحلة الرابعة', 'role': 'architect_id'},
        {'code': 'rn_4_5', 'name': '5- تجهيز الكراسة النهائية', 'stage': 'المرحلة الرابعة', 'role': 'secretary_id'},
        {'code': 'rn_5_1', 'name': '1- إصدار تعهد الإشراف', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
        {'code': 'rn_5_2', 'name': '2- الإشراف على التنفيذ', 'stage': 'المرحلة الخامسة', 'role': 'structural_id'},
        {'code': 'rn_5_3', 'name': '3- كتب البنك', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
        {'code': 'rn_5_4', 'name': '4- إنهاء الإشراف', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
    ],
    'non_res_new':[
        {'code': 'nrn_1_1', 'name': '1- تصميم الكروكي', 'stage': 'المرحلة الأولى', 'role': 'architect_id'},
        {'code': 'nrn_1_2', 'name': '2- تجميع المستندات', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'nrn_1_3', 'name': '3- العقد وتحصيل الدفعة الأولى', 'stage': 'المرحلة الأولى', 'role': 'accountant_id'},
        {'code': 'nrn_1_4', 'name': '4- تجهيز النماذج والتعهدات والتوقيع', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'nrn_1_5', 'name': '5- فحص التربة - كتاب الكهرباء', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'nrn_2_1', 'name': '1- سيستم الأعمدة', 'stage': 'المرحلة الثانية', 'role': 'structural_id'},
        {'code': 'nrn_2_2', 'name': '2- الواجهات', 'stage': 'المرحلة الثانية', 'role': 'facade_draftsman_id'},
        {'code': 'nrn_2_3', 'name': '3- رسم مخطط البلدية', 'stage': 'المرحلة الثانية', 'role': 'muni_draftsman_id'},
        {'code': 'nrn_3_1', 'name': '1- إرسال للمطافي', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nrn_3_2', 'name': '2- اعتماد المطافي', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nrn_3_3', 'name': '3- إرسال للتنظيم', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nrn_3_4', 'name': '4- اعتماد التنظيم', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nrn_3_5', 'name': '5- إرسال للبلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nrn_3_6', 'name': '6- اعتماد البلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nrn_3_7', 'name': '7- تحصيل الدفعة الأخيرة من العقد', 'stage': 'المرحلة الثالثة', 'role': 'accountant_id'},
        {'code': 'nrn_4_1', 'name': '1- تصميم المخطط الإنشائي', 'stage': 'المرحلة الرابعة', 'role': 'structural_id'},
        {'code': 'nrn_4_2', 'name': '2- تصميم مخطط الصحي', 'stage': 'المرحلة الرابعة', 'role': 'draftsman_id'},
        {'code': 'nrn_4_3', 'name': '5- تجهيز الكراسة النهائية', 'stage': 'المرحلة الرابعة', 'role': 'secretary_id'},
        {'code': 'nrn_5_1', 'name': '1- إصدار تعهد الإشراف', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
        {'code': 'nrn_5_2', 'name': '2- الإشراف على التنفيذ', 'stage': 'المرحلة الخامسة', 'role': 'structural_id'},
        {'code': 'nrn_5_3', 'name': '4- إنهاء الإشراف', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
    ],
    'res_add':[
        {'code': 'ra_1_1', 'name': '1- دراسة المخطط الإنشائي القديم', 'stage': 'المرحلة الأولى', 'role': 'structural_id'},
        {'code': 'ra_1_2', 'name': '2- كشف على العقار', 'stage': 'المرحلة الأولى', 'role': 'architect_id'},
        {'code': 'ra_1_3', 'name': '3- كروكي', 'stage': 'المرحلة الأولى', 'role': 'architect_id'},
        {'code': 'ra_1_4', 'name': '4- جمع الوثائق والمستندات', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'ra_1_5', 'name': '5- العقد وتحصيل الدفعة الأولى', 'stage': 'المرحلة الأولى', 'role': 'accountant_id'},
        {'code': 'ra_2_1', 'name': '1- سيستم الأعمدة', 'stage': 'المرحلة الثانية', 'role': 'structural_id'},
        {'code': 'ra_2_2', 'name': '2- رسم البلدية', 'stage': 'المرحلة الثانية', 'role': 'muni_draftsman_id'},
        {'code': 'ra_3_1', 'name': '1- إرسال للبلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'ra_3_2', 'name': '2- اعتماد البلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'ra_3_3', 'name': '3- تحصيل الدفعة الأخيرة من العقد', 'stage': 'المرحلة الثالثة', 'role': 'accountant_id'},
        {'code': 'ra_4_1', 'name': '1- مخطط إنشائي كامل', 'stage': 'المرحلة الرابعة', 'role': 'structural_id'},
        {'code': 'ra_4_2', 'name': '2- تجهيز الكراسة النهائية', 'stage': 'المرحلة الرابعة', 'role': 'secretary_id'},
        {'code': 'ra_5_1', 'name': '1- الإشراف على التنفيذ', 'stage': 'المرحلة الخامسة', 'role': 'structural_id'},
        {'code': 'ra_5_2', 'name': '2- كتب البنك', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
        {'code': 'ra_5_3', 'name': '3- إنهاء الإشراف', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
    ],
    'non_res_add':[
        {'code': 'nra_1_1', 'name': '1- دراسة المخطط الإنشائي القديم', 'stage': 'المرحلة الأولى', 'role': 'structural_id'},
        {'code': 'nra_1_2', 'name': '2- كشف على العقار', 'stage': 'المرحلة الأولى', 'role': 'architect_id'},
        {'code': 'nra_1_3', 'name': '3- كروكي', 'stage': 'المرحلة الأولى', 'role': 'architect_id'},
        {'code': 'nra_1_4', 'name': '4- جمع الوثائق والمستندات', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'nra_1_5', 'name': '5- العقد وتحصيل الدفعة الأولى', 'stage': 'المرحلة الأولى', 'role': 'accountant_id'},
        {'code': 'nra_2_1', 'name': '1- سيستم الأعمدة', 'stage': 'المرحلة الثانية', 'role': 'structural_id'},
        {'code': 'nra_2_2', 'name': '2- رسم البلدية', 'stage': 'المرحلة الثانية', 'role': 'muni_draftsman_id'},
        {'code': 'nra_3_1', 'name': '1- إرسال للمطافي', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nra_3_2', 'name': '2- اعتماد للمطافي', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nra_3_3', 'name': '3- إرسال للتنظيم', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nra_3_4', 'name': '4- اعتماد التنظيم', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nra_3_5', 'name': '5- إرسال للبلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nra_3_6', 'name': '6- اعتماد البلدية', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
        {'code': 'nra_3_7', 'name': '7- تحصيل الدفعة الأخيرة من العقد', 'stage': 'المرحلة الثالثة', 'role': 'accountant_id'},
        {'code': 'nra_4_1', 'name': '1- مخطط إنشائي كامل', 'stage': 'المرحلة الرابعة', 'role': 'structural_id'},
        {'code': 'nra_4_2', 'name': '2- تجهيز الكراسة النهائية', 'stage': 'المرحلة الرابعة', 'role': 'secretary_id'},
        {'code': 'nra_5_1', 'name': '1- الإشراف على التنفيذ', 'stage': 'المرحلة الخامسة', 'role': 'structural_id'},
        {'code': 'nra_5_2', 'name': '3- إنهاء الإشراف', 'stage': 'المرحلة الخامسة', 'role': 'secretary_id'},
    ],
    'demolition':[
        {'code': 'dem_1_1', 'name': '1- تجميع المستندات والوثائق', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'dem_1_2', 'name': '2- العقد وتحصيل الدفعة الأولى', 'stage': 'المرحلة الأولى', 'role': 'accountant_id'},
        {'code': 'dem_1_3', 'name': '3- توقيع نماذج البلدية', 'stage': 'المرحلة الأولى', 'role': 'secretary_id'},
        {'code': 'dem_1_4', 'name': '4- كتاب المواصفات وكتاب قطع تربة', 'stage': 'المرحلة الأولى', 'role': 'architect_id'},
        {'code': 'dem_2_1', 'name': '1- إرسال للبلدية', 'stage': 'المرحلة الثانية', 'role': 'secretary_id'},
        {'code': 'dem_2_2', 'name': '2- اعتماد البلدية', 'stage': 'المرحلة الثانية', 'role': 'secretary_id'},
        {'code': 'dem_3_1', 'name': '1- الإشراف على الهدم', 'stage': 'المرحلة الثالثة', 'role': 'structural_id'},
        {'code': 'dem_3_2', 'name': '2- إنهاء الإشراف', 'stage': 'المرحلة الثالثة', 'role': 'secretary_id'},
    ]
}

# ==============================================================================
#  HELPER FUNCTIONS FOR GOVERNORATE & REGION 
# ==============================================================================
def _get_governorate_areas():
    return {
        'محافظة العاصمة':[
            ('جابر الاحمد', 'جابر الاحمد'), ('القبلة', 'القبلة'), ('الشرق', 'الشرق'),
            ('المرقاب', 'المرقاب'), ('الصالحية', 'الصالحية'), ('دسمان', 'دسمان'),
            ('الدعية', 'الدعية'), ('الدسمة', 'الدسمة'), ('كيفان', 'كيفان'),
            ('الخالدية', 'الخالدية'), ('الشامية', 'الشامية'), ('الروضة', 'الروضة'),
            ('العديلية', 'العديلية'), ('الفيحاء', 'الفيحاء'), ('القادسية', 'القادسية'),
            ('قرطبة', 'قرطبة'), ('السرة', 'السرة'), ('اليرموك', 'اليرموك'),
            ('النزهة', 'النزهة'), ('الشويخ الصناعية 1', 'الشويخ الصناعية 1'),
            ('الشويخ الصناعية 2', 'الشويخ الصناعية 2'), ('الشويخ الصناعية 3', 'الشويخ الصناعية 3'),
            ('الشويخ الادارية', 'الشويخ الادارية'), ('الشويخ السكنى', 'الشويخ السكنى'),
            ('الشويخ التعليمية', 'الشويخ التعليمية'), ('الشويخ الصحيه', 'الشويخ الصحيه'),
            ('الواجهه البحرية', 'الواجهه البحرية'), ('غرناطة', 'غرناطة'),
            ('الصليبيخات', 'الصليبيخات'), ('المنصورية', 'المنصورية'),
            ('الدوحة السكنيه', 'الدوحة السكنيه'), ('الرى', 'الرى'),
            ('ميناء الدوحة', 'ميناء الدوحة'), ('جزيره عوهه', 'جزيره عوهه'),
            ('جزيره فيلكه', 'جزيره فيلكه'), ('جزيره مسكان', 'جزيره مسكان'),
            ('حدائق السور – الحزام الاخضر', 'حدائق السور – الحزام الاخضر'),
            ('بنيد القار', 'بنيد القار'), ('ميناء الشويخ', 'ميناء الشويخ'),
            ('معسكرات المباركيه – جيوان', 'معسكرات المباركيه – جيوان'),
            ('شاليهات الدوحة', 'شاليهات الدوحة'), ('السره', 'السره'),
        ],
        'محافظة حولي':[
            ('حولي', 'حولي'), ('السالمية', 'السالمية'), ('الرميثية', 'الرميثية'),
            ('الجابرية', 'الجابرية'), ('بيان', 'بيان'), ('مشرف', 'مشرف'),
            ('سلوى', 'سلوى'), ('ميدان حولي', 'ميدان حولي'), ('الزهراء', 'الزهراء'),
            ('الصديق', 'الصديق'), ('حطين', 'حطين'), ('السلام', 'السلام'),
            ('الشهداء', 'الشهداء'), ('انجفة', 'انجفة'), ('الشعب', 'الشعب'),
            ('مبارك العبد الله', 'مبارك العبد الله'), ('الواجهه البحريه', 'الواجهه البحريه'),
            ('الضاحيه الدبلوماسيه', 'الضاحيه الدبلوماسيه'),
            ('المباركيه قطعة 15 بيان', 'المباركيه قطعة 15 بيان'), ('البدع', 'البدع'),
        ],
        'محافظة الفروانية':[
            ('الفروانية', 'الفروانية'), ('خيطان', 'خيطان'), ('العمرية', 'العمرية'),
            ('الرحاب', 'الرحاب'), ('الرقعى', 'الرقعى'), ('الشدادية', 'الشدادية'),
            ('الضجيج', 'الضجيج'), ('المطار', 'المطار'),
            ('غرب الجليب الشداديه', 'غرب الجليب الشداديه'),
            ('عبد الله المبارك', 'عبد الله المبارك'),
            ('مدينه صباح السالم الجامعية', 'مدينه صباح السالم الجامعية'),
            ('منطقة المعارض جنوب خيطان', 'منطقة المعارض جنوب خيطان'),
            ('الأندلس', 'الأندلس'), ('إشبيلية', 'إشبيلية'),
            ('جليب الشيوخ', 'جليب الشيوخ'), ('الفردوس', 'الفردوس'),
            ('صباح الناصر', 'صباح الناصر'), ('الرابية', 'الرابية'),
            ('العارضية', 'العارضية'),
            ('العارضية استعمالات حكومية', 'العارضية استعمالات حكومية'),
            ('العارضية مخازن', 'العارضية مخازن'), ('العارضية الحرفية', 'العارضية الحرفية'),
            ('غرب عبد المبارك السكنى', 'غرب عبد المبارك السكنى'),
            ('جنوب عبد الله المبارك السكنى', 'جنوب عبد الله المبارك السكنى'),
            ('العباسية', 'العباسية'),
        ],
        'محافظة الأحمدي':[
            ('الأحمدي', 'الأحمدي'), ('الفحيحيل', 'الفحيحيل'), ('المنقف', 'المنقف'),
            ('أبو حليفة', 'أبو حليفة'), ('الصباحية', 'الصباحية'), ('الرقة', 'الرقة'),
            ('هدية', 'هدية'), ('الفنطاس', 'الفنطاس'), ('المهبولة', 'المهبولة'),
            ('العقيلة', 'العقيلة'), ('الظهر', 'الظهر'), ('جابر العلي', 'جابر العلي'),
            ('صباح الأحمد السكنية', 'صباح الأحمد السكنية'), ('الوفرة', 'الوفرة'),
            ('الخيران', 'الخيران'), ('ميناء الزور', 'ميناء الزور'),
            ('ميناء عبد الله الصناعية', 'ميناء عبد الله الصناعية'),
            ('ميناء عبد الله', 'ميناء عبد الله'), ('مزارع الوفره', 'مزارع الوفره'),
            ('صباح الاحمد السكنيه', 'صباح الاحمد السكنيه'),
            ('صباح الاحمد البحريه', 'صباح الاحمد البحريه'),
            ('قردان والحفيرة والفوار', 'قردان والحفيرة والفوار'),
            ('فهد الاحمد', 'فهد الاحمد'),
            ('على صباح السالم – ام الهيمان', 'على صباح السالم – ام الهيمان'),
            ('عريفجان', 'عريفجان'), ('ضليع الزنيف', 'ضليع الزنيف'),
            ('شرق الاحمدى الخدميه والحرفية والتجاريه', 'شرق الاحمدى الخدميه والحرفية والتجاريه'),
            ('شرق الاحمدى', 'شرق الاحمدى'),
            ('شاليهات ميناء عبد الله', 'شاليهات ميناء عبد الله'),
            ('شاليهات بنيدر', 'شاليهات بنيدر'),
            ('شاليهات النويصيب', 'شاليهات النويصيب'),
            ('شاليهات الضاعيه', 'شاليهات الضاعيه'), ('شاليهات الزور', 'شاليهات الزور'),
            ('شاليهات الخيران', 'شاليهات الخيران'),
            ('شاليهات الجليعه', 'شاليهات الجليعه'),
            ('رجم خشمان ومصلان', 'رجم خشمان ومصلان'),
            ('جنوب الصباحية', 'جنوب الصباحية'), ('برقان', 'برقان'),
            ('الوفره السكنيه', 'الوفره السكنيه'),
            ('الهيئة العامة للزراعة والثورة السمكيه – مزارع', 'الهيئة العامة للزراعة والثورة السمكيه – مزارع'),
            ('النويصيب', 'النويصيب'), ('المقوع', 'المقوع'), ('الفحيحيل', 'الفحيحيل'),
            ('العبدليه', 'العبدليه'),
            ('الصناعية الصناعية الخلط الجاهز', 'الصناعية الصناعية الخلط الجاهز'),
            ('الشعيبة الصناعية الشرقيه', 'الشعيبة الصناعية الشرقيه'),
            ('الشعيبة الصناعية الغربيه', 'الشعيبة الصناعية الغربيه'),
            ('الشعيبة', 'الشعيبة'), ('الشدادية الصناعية', 'الشدادية الصناعية'),
            ('الزور وصوله', 'الزور وصوله'), ('ام حجول', 'ام حجول'),
            ('ام قدير', 'ام قدير'), ('ابو خرجين والصبيحية', 'ابو خرجين والصبيحية'),
        ],
        'محافظة الجهراء':[
            ('الجهراء', 'الجهراء'), ('القصر', 'القصر'), ('النسيم', 'النسيم'),
            ('الواحة', 'الواحة'), ('النعيم', 'النعيم'), ('تيماء', 'تيماء'),
            ('سعد العبدالله', 'سعد العبدالله'), ('الصليبية', 'الصليبية'),
            ('كبد', 'كبد'), ('المطلاع', 'المطلاع'), ('أمغرة', 'أمغرة'),
            ('البحيث', 'البحيث'), ('الجهراء الصناعية الثانية', 'الجهراء الصناعية الثانية'),
            ('الجهراء الصناعية الحرفيه الاولى', 'الجهراء الصناعية الحرفيه الاولى'),
            ('الرتقة والحريجه', 'الرتقة والحريجه'),
            ('الرحية وام توينج', 'الرحية وام توينج'), ('الروضتين', 'الروضتين'),
            ('السالمى', 'السالمى'), ('السكراب', 'السكراب'),
            ('الشقايا – الدبدبة – المتياهه', 'الشقايا – الدبدبة – المتياهه'),
            ('الصابرية – العرفجية', 'الصابرية – العرفجية'),
            ('الصبية', 'الصبية'), ('الصليبية الزراعية', 'الصليبية الزراعية'),
            ('الصليبيه السكنية', 'الصليبيه السكنية'),
            ('الصليبية الصناعية 2', 'الصليبية الصناعية 2'),
            ('الصليبيه الصناعية 1', 'الصليبيه الصناعية 1'),
            ('الصير وام المدفاع', 'الصير وام المدفاع'), ('العبدلى', 'العبدلى'),
            ('العبدلى وصخيبريات', 'العبدلى وصخيبريات'), ('العيون', 'العيون'),
            ('القيروان – جنوب الدوحة', 'القيروان – جنوب الدوحة'),
            ('المستثمر الاجنبى (منطقة العبدلى الاقتصادية )', 'المستثمر الاجنبى (منطقة العبدلى الاقتصادية )'),
            ('المطلاع وجال الاطراف', 'المطلاع وجال الاطراف'),
            ('النعايم الصناعية', 'النعايم الصناعية'),
            ('النهضة – شرق الصليبخات', 'النهضة – شرق الصليبخات'),
            ('امغره الصناعية', 'امغره الصناعية'), ('تيماء', 'تيماء'),
            ('جال الزور', 'جال الزور'), ('جزيرة ام المرادم', 'جزيرة ام المرادم'),
            ('جزيره ام النمل', 'جزيره ام النمل'), ('جزيرة بوبيان', 'جزيرة بوبيان'),
            ('جزيرة قارووه', 'جزيرة قارووه'), ('جزيرة كبر', 'جزيرة كبر'),
            ('جزيرة وربة', 'جزيرة وربة'), ('جنوب امغرة', 'جنوب امغرة'),
            ('شرق الجهراء', 'شرق الجهراء'), ('شرق تيماء', 'شرق تيماء'),
            ('شمال غرب الجهراء', 'شمال غرب الجهراء'),
            ('قلمة شايع والمناقيش', 'قلمة شايع والمناقيش'),
            ('كاظمة', 'كاظمة'), ('كبد والشق والضبعة', 'كبد والشق والضبعة'),
            ('معسكرات الجهراء', 'معسكرات الجهراء'), ('مقبرة', 'مقبرة'),
            ('مناطق نائية -الجهراء', 'مناطق نائية -الجهراء'),
        ],
        'محافظة مبارك الكبير':[
            ('مبارك الكبير', 'مبارك الكبير'), ('العدان', 'العدان'),
            ('القرين', 'القرين'), ('القصور', 'القصور'), ('المسيلة', 'المسيلة'),
            ('غرب أبو فطيرة', 'غرب أبو فطيرة'), ('الفنيطيس', 'الفنيطيس'),
            ('المسايل', 'المسايل'), ('الوسطى', 'الوسطى'),
            ('جنوب الوسطى', 'جنوب الوسطى'), ('صباح السالم', 'صباح السالم'),
            ('صبحان الصناعية', 'صبحان الصناعية'),
            ('ضاحية ابو فطيرة', 'ضاحية ابو فطيرة'), ('ابو الحصانية', 'ابو الحصانية'),
        ],
    }

# ==============================================================================
#  SALE ORDER MODEL 
# ==============================================================================
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    building_type = fields.Selection([
        ('residential', 'سكن خاص'), 
        ('investment', 'استثماري'), 
        ('commercial', 'تجاري'), 
        ('industrial', 'صناعي'), 
        ('cooperative', 'جمعيات وتعاونيات'), 
        ('mosque', 'مساجد'), 
        ('hangar', 'مخازن / شبرات'), 
        ('farm', 'مزارع')
    ], string="نوع العقار")
    
    service_type = fields.Selection([
        ('new_construction', 'بناء جديد'), 
        ('demolition', 'هدم'), 
        ('modification', 'تعديل'), 
        ('addition', 'اضافة'), 
        ('addition_modification', 'تعديل واضافة')
    ], string="نوع الخدمة")

    plot_no = fields.Char(string="رقم القسيمة")
    block_no = fields.Char(string="القطعة")
    street_no = fields.Char(string="الضاحيه")
    area = fields.Char(string="مساحة الارض")
    electricity_receipt = fields.Char(string="ايصال تيار كهربا")
    
    project_id = fields.Many2one('project.project', string='Project', copy=False)
    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة")
    region_id = fields.Many2one('kuwait.region', string="المنطقة")

    quotation_stage_id = fields.Many2one(
        'engineering.quotation.stage',
        string='Quotation Stage',
        tracking=True,
        default=lambda self: self.env['engineering.quotation.stage'].search([], order='sequence', limit=1)
    )

    def _create_engineering_project(self):
        self.ensure_one()
        project_vals = {
            'name': f"{self.name} - {self.partner_id.name}",
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id,
            'building_type': self.building_type,
            'service_type': self.service_type,
            'plot_no': self.plot_no,
            'block_no': self.block_no,
            'street_no': self.street_no,
            'area': self.area,
            'governorate_id': self.governorate_id.id, 
            'region_id': self.region_id.id,
            'electricity_receipt': self.electricity_receipt,
        }
        project = self.env['project.project'].create(project_vals)
        
        stages = ['المرحلة الأولى', 'المرحلة الثانية', 'المرحلة الثالثة', 'المرحلة الرابعة', 'المرحلة الخامسة']
        for index, stage_name in enumerate(stages):
            self.env['project.task.type'].create({
                'name': stage_name, 'project_ids': [(4, project.id)], 'sequence': index + 1
            })
            
        self.write({'project_id': project.id})
        return project

# ==============================================================================
#  PROJECT MODEL
# ==============================================================================
class ProjectProject(models.Model):
    _inherit = 'project.project'

    sale_order_id = fields.Many2one('sale.order', string='Source Quotation', readonly=True)
    building_type = fields.Selection([
        ('residential', 'سكن خاص'), ('investment', 'استثماري'), 
        ('commercial', 'تجاري'), ('industrial', 'صناعي')
    ], string="نوع المبنى")
    
    service_type = fields.Selection([
        ('new_construction', 'بناء جديد'), ('demolition', 'هدم'), 
        ('modification', 'تعديل'), ('addition', 'اضافة'), 
        ('addition_modification', 'تعديل واضافة')
    ], string="نوع الخدمة")

    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة")
    region_id = fields.Many2one('kuwait.region', string="المنطقة")
    plot_no = fields.Char(string="رقم القسيمة")
    block_no = fields.Char(string="القطعة")
    street_no = fields.Char(string="الضاحيه")
    area = fields.Char(string="المساحة (Area)")
    electricity_receipt = fields.Char(string="ايصال تيار كهربا") 

    architect_id = fields.Many2one('res.users', string="المهندس المعماري")
    accountant_id = fields.Many2one('res.users', string="المحاسبة")
    structural_id = fields.Many2one('res.users', string="المهندس الإنشائي")
    facade_draftsman_id = fields.Many2one('res.users', string="رسام الواجهات")
    secretary_id = fields.Many2one('res.users', string="السكرتارية")
    muni_draftsman_id = fields.Many2one('res.users', string="رسام البلدية")
    electrical_id = fields.Many2one('res.users', string="مهندس الكهرباء")
    draftsman_id = fields.Many2one('res.users', string="الرسام (صحي/مخططات)")

    workflow_started = fields.Boolean(default=False)
    triggered_steps = fields.Text(string="المهام المنفذة", default="")
    commitment_ids = fields.Many2many('sale.order.line', string='Commitments', copy=False)

    def _get_workflow_key(self):
        self.ensure_one()
        if self.service_type == 'demolition': return 'demolition'
        is_addition = self.service_type in ['addition', 'modification', 'addition_modification']
        if self.building_type == 'residential':
            return 'res_add' if is_addition else 'res_new'
        return 'non_res_add' if is_addition else 'non_res_new'

    def action_start_workflow(self):
        self.ensure_one()
        if self.workflow_started:
            raise UserError(_("تم بدء سير العمل مسبقاً!"))

        wf_key = self._get_workflow_key()
        workflow = WORKFLOW_TEMPLATES.get(wf_key, [])
        if not workflow:
            raise UserError(_("لا توجد خطة مهام مطابقة."))

        for index, step in enumerate(workflow):
            # المهمة الأولى فقط مفعلة، الباقي معطل
            is_disabled = (index != 0)
            self._create_task_for_step(step, is_disabled=is_disabled)

        self.workflow_started = True

    def _trigger_next_workflow_step(self, completed_code):
        self.ensure_one()
        wf_key = self._get_workflow_key()
        workflow = WORKFLOW_TEMPLATES.get(wf_key, [])
        for i, step in enumerate(workflow):
            if step['code'] == completed_code:
                if i + 1 < len(workflow):
                    next_step = workflow[i + 1]
                    next_task = self.env['project.task'].search([
                        ('project_id', '=', self.id),
                        ('workflow_step', '=', next_step['code'])
                    ], limit=1)
                    if next_task:
                        next_task.is_disabled = False
                break

    def _create_task_for_step(self, step_data, is_disabled=False):
        stages = self.env['project.task.type'].search([
            ('project_ids', 'in', self.id), ('name', '=', step_data['stage'])
        ], limit=1)
        
        user_id = getattr(self, step_data['role']).id if hasattr(self, step_data['role']) and getattr(self, step_data['role']) else False
        
        # حساب الترتيب Sequence لضمان الترتيب الصحيح داخل المرحلة
        wf_key = self._get_workflow_key()
        workflow = WORKFLOW_TEMPLATES.get(wf_key, [])
        tasks_in_stage = [t for t in workflow if t['stage'] == step_data['stage']]
        task_seq = 10
        for idx, t in enumerate(tasks_in_stage):
            if t['code'] == step_data['code']:
                task_seq = idx + 1
                break

        self.env['project.task'].create({
            'name': step_data['name'],
            'project_id': self.id,
            'stage_id': stages.id if stages else False,
            'workflow_step': step_data['code'],
            'sequence': task_seq,
            'is_disabled': is_disabled,
            'user_ids': [(4, user_id)] if user_id else False,
        })

# ==============================================================================
#  PROJECT TASK MODEL
# ==============================================================================
class ProjectTask(models.Model):
    _inherit = 'project.task'

    workflow_step = fields.Char(string="Workflow Trigger", readonly=True)
    is_disabled = fields.Boolean(string="مقفلة (Disabled)", default=False)
    phase_ids = fields.One2many('project.task.phase', 'task_id', string='مراحل التنفيذ (Phases)')

    def write(self, vals):
        # منع نقل المهمة المنجزة إذا كانت مقفلة
        done_stage = self.env.ref('project.project_stage_3', raise_if_not_found=False)
        
        if 'stage_id' in vals and done_stage and vals['stage_id'] == done_stage.id:
            for task in self:
                if task.is_disabled:
                    raise UserError(_("لا يمكنك إنجاز هذه المهمة لأنها مقفلة! يرجى إتمام المهام السابقة أولاً."))

        res = super(ProjectTask, self).write(vals)
        
        # تفعيل المهمة التالية عند الانتهاء
        if 'stage_id' in vals and done_stage and vals['stage_id'] == done_stage.id:
            for task in self:
                if task.workflow_step and task.project_id:
                    task.project_id._trigger_next_workflow_step(task.workflow_step)
        return res

# ==============================================================================
#  LOCATION MODELS 
# ==============================================================================
class KuwaitGovernorate(models.Model):
    _name = 'kuwait.governorate'
    _description = 'Kuwait Governorate'
    name = fields.Char(string='المحافظة', required=True)

class KuwaitRegion(models.Model):
    _name = 'kuwait.region'
    _description = 'Kuwait Region'
    name = fields.Char(string='المنطقة', required=True)
    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة", required=True)
    
class ProjectTaskPhase(models.Model):
    _name = 'project.task.phase'
    _description = 'Task Construction Phase Checklist'
    _order = 'sequence, id'
    task_id = fields.Many2one('project.task', string='Task', ondelete='cascade')
    sequence = fields.Integer(string='التسلسل', default=10)
    floor_category = fields.Char(string='الدور (Floor)', required=True)
    name = fields.Char(string='المرحلة (Phase)', required=True)
    is_completed = fields.Boolean(string='تم (Completed)', default=False)

class EngineeringQuotationStage(models.Model):
    _name = 'engineering.quotation.stage'
    _description = 'Engineering Quotation Stage'
    _order = 'sequence, id'
    name = fields.Char(string='اسم المرحلة', required=True)
    sequence = fields.Integer(default=10)
    next_stage_id = fields.Many2one('engineering.quotation.stage', string="المرحلة التالية")
    button_name = fields.Char(string="نص الزر")
    is_approved_stage = fields.Boolean(string="مرحلة الموافقة؟")
