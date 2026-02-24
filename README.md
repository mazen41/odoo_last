# Engineering Office ERP - Odoo 17 Custom Modules

نظام إدارة المكتب الهندسي المتكامل - الكويت

## Modules Included

| Module | Description |
|--------|-------------|
| `engineering_core` | Base fields on res.partner, crm.lead, sale.order (building_type, service_type, plot_no, etc.) |
| `engineering_quotation` | 7-stage quotation pipeline, 50KD opening fee, manual project creation |
| `engineering_reports` | Site visit reports with WhatsApp integration |
| `engineering_project` | Project enhancements linked to sale.order |
| `engineering_documents` | Document management, PDF contract reports |
| `engineering_contracts` | Full contract system with templates, sequence EC-YYYY/ |
| `engineering_packages` | Service packages (basic/premium/gold/supervision) |

## Dependencies

These modules depend on standard Odoo 17 modules:
- `crm`
- `sale_management`
- `sale_project`
- `project`
- `account`

## Installation on Odoo.sh

1. Connect this repository to your Odoo.sh project
2. The modules will be automatically detected
3. Install `engineering_core` first, then the other modules

## Features

- **7-Stage Quotation Pipeline**: استلام → مراجعة → تسعير → إرسال → تفاوض → مقبول → مرفوض
- **Opening Fee Management**: 50 KD invoice + deduction
- **Manual Project Creation**: From approved quotations
- **Contract Templates**: Auto-selected based on building/service type
- **WhatsApp Integration**: Send quotations, contracts, reports via WhatsApp
- **PDF Reports**: Professional Arabic/English PDF generation
- **Site Visit Reports**: Upload and send to customers

## License

LGPL-3
