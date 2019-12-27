# -*- coding: utf-8 -*-
from odoo import models, fields, api

#--------------------------------Test Models------------------------------------#

class persontocargo(models.Model):
    _name = 'testlogyca.persontocargo'
    _description = 'Prueba de relación padre hijo (Empleados)'

    name = fields.Char(string='Nombre', required=True)
    age = fields.Integer(string='Edad', required=True)
    date = fields.Date(string="Fecha de nacimiento", required=True)
    gender = fields.Selection([('1', 'Masculino'), ('2', 'Femenino'), ('3', 'Otro')], string='Genero', required=True)

class testlogyca(models.Model):
    _name = 'testlogyca.testlogyca'
    _description = 'Prueba de relación padre hijo (Lideres)'

    name = fields.Char(string='Nombre', required=True)
    age = fields.Integer(string='Edad', required=True)
    photo = fields.Binary(string='Foto', required=True)
    date = fields.Date(string="Fecha de nacimiento", required=True)
    gender = fields.Selection([('1', 'Masculino'), ('2', 'Femenino'), ('3', 'Otro')], string='Genero', required=True)
    nationality = fields.Many2one('res.country', string='Nacionalidad')
    is_company = fields.Boolean(string='Es compañia')
    active = fields.Boolean(string='Activo')
    salary = fields.Float(string='Salario mensual')
    salary_for_day = fields.Float(compute="_salary_day", string='Salario por dia')
    date_register = fields.Date(string='Fecha de registro', compute='_date_today')
    persontocargo = fields.Many2many('testlogyca.persontocargo', string='Personas a cargo')
    description = fields.Text(string='Observaciones')

    @api.depends('salary')
    def _salary_day(self):
        self.salary_for_day = self.salary / 30
        

    @api.depends('date')
    def _date_today(self):
        self.date_register = fields.Date.today()

#--------------------------------Modelos propios de Logyca------------------------------------#

# CIUDAD
class x_city(models.Model):
    _name = 'testlogyca.city'
    _description = 'Ciudades por departamento'

    state_id = fields.Many2one('res.country.state', string='Departamento', required=True)
    code = fields.Char(string='Código', size=10, required=True)
    name = fields.Char(string='Nombre', required=True)

# CIIU
class ciiu(models.Model):
    _name = 'testlogyca.ciiu'
    _parent_store = True
    _parent_name  = 'parent_id'
    _description = 'CIIU - Actividades economicas'

    code = fields.Char('Codigo', required=True)
    name = fields.Char('Name', required=True)
    parent_id = fields.Many2one('testlogyca.ciiu','Parent Tag', ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('testlogyca.ciiu', 'parent_id', 'Child Tags')    
    
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.name)))
        return result

# SECTORES
class x_sectors(models.Model):
    _name = 'testlogyca.sectors'
    _description = 'Sectores'

    code = fields.Char(string='Código', size=10,required=True)
    name = fields.Char(string='Nombre', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.name)))
        return result

# SUBSECTORES
class x_subsectors(models.Model):
    _name = 'testlogyca.subsectors'
    _description = 'Sub-Sectores'

    sector_id = fields.Many2one('testlogyca.sectors', string='Sector principal', required=True)
    code = fields.Char(string='Código', size=10, required=True)
    name = fields.Char(string='Nombre', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.name)))
        return result

# TIPOS DE VINCULACION
class x_vinculation_types(models.Model):
    _name = 'testlogyca.vinculation_types'
    _description = 'Tipos de vinculación'

    code = fields.Char(string='Código', size=10, required=True)
    name = fields.Char(string='Nombre', size=100, required=True)
    active = fields.Boolean(string='Activo')
    novelty = fields.Selection([('1', 'Vigente'), ('2', 'No esta vigente para nuevos - se mantiene para las empresas que lo adquirieron')], string='Novedad', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.name)))
        return result

# RESPONSABILIDADES RUT
class x_responsibilities_rut(models.Model):
    _name = 'testlogyca.responsibilities_rut'
    _description = 'Responsabilidades RUT'

    code = fields.Char(string='Identificador', size=5, required=True)
    description = fields.Char(string='Descripción', size=100, required=True)
    valid_for_fe = fields.Boolean(string='Valido para facturación electrónica')
    
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.description)))
        return result

# TIPOS DE CONTACTO
class x_contact_types(models.Model):
    _name = 'testlogyca.contact_types'
    _description = 'Tipos de contacto'
    
    code = fields.Char(string='Código', size=10, required=True)
    name = fields.Char(string='Nombre', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.name)))
        return result

# CARGOS
class x_job_title(models.Model):
    _name = 'testlogyca.job_title'
    _description = 'Cargos'

    code = fields.Char(string='Código', size=10, required=True)
    name = fields.Char(string='Nombre', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.name)))
        return result

# ÁREAS
class x_areas(models.Model):
    _name = 'testlogyca.areas'
    _description = 'Áreas'

    code = fields.Char(string='Código', size=10, required=True)
    name = fields.Char(string='Nombre', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} | {}".format(record.code, record.name)))
        return result

#---------------------------Modelos existentes de Odoo modificados por Logyca-------------------------------#

class ResPartner(models.Model):
    _inherit = 'res.partner'
    #INFORMACION BASICA CLIENTE
    x_active_for_logyca = fields.Boolean(string='Activo')
    x_document_type = fields.Selection([
                                        ('11', 'Registro civil de nacimiento'), 
                                        ('12', 'Tarjeta de identidad'), 
                                        ('13', 'Cédula de ciudadania'),
                                        ('21', 'Tarjeta de extranjería'),
                                        ('22', 'Cedula de extranjería'),
                                        ('31', 'NIT'),
                                        ('41', 'Pasaporte'),
                                        ('42', 'Tipo de documento extranjero'),
                                        ('43', 'Sin identificación del exterior o para uso definido por la DIAN')
                                    ], string='Tipo de documento')
    x_digit_verification = fields.Integer(string='Digito de verificación')
    x_first_name = fields.Char(string='Primer nombre')
    x_second_name = fields.Char(string='Segundo nombre')
    x_first_lastname = fields.Char(string='Primer apellido')
    x_second_lastname = fields.Char(string='Segundo apellido')
    x_is_main_contact = fields.Boolean(string='¿Es contacto principal?')
    x_is_member_directive = fields.Boolean(string='¿Es miembro del Consejo Directivo?')

    #UBICACIÓN PRINCIPAL
    x_city = fields.Many2one('testlogyca.city', string='Ciudad')

    #CLASIFICACION 
    x_organization_type = fields.Selection([('01', 'Empresa'), ('02', 'Universidad'), ('03', 'Centro de investigación'), ('04', 'Multilateral')], string='Tipo de organización')
    x_entity_type = fields.Selection([('01', 'Pública'), ('02', 'Privada')], string='Tipo de entidad')
    #x_economic_activity = fields.Selection([('01', 'Comercio'), ('02', 'Manufactura'), ('03', 'Servicio')], string='Actividad económica general') - Se comenta el campo 
    x_sector_id = fields.Many2one('testlogyca.sectors', string='Sector')
    x_subsector_id = fields.Many2one('testlogyca.subsectors', string='Sub-sector')
    x_ciiu_activity = fields.Many2one('testlogyca.ciiu', string='Código CIIU actividad Principal')
    x_ciiu_activity_second = fields.Many2one('testlogyca.ciiu', string='Código CIIU actividad Secundaria')

    #GRUPO EMPRESARIAL
    x_is_business_group = fields.Boolean(string='¿Es un Grupo Empresarial?')

    #VINCULACION CON LOGYCA
    x_active_vinculation = fields.Boolean(string='Estado de la vinculación') 
    x_date_vinculation = fields.Date(string="Fecha de vinculación")
    x_type_vinculation = fields.Many2many('testlogyca.vinculation_types', string='Tipo de vinculación')
    x_sponsored = fields.Boolean(string='Patrocinado')
    x_flagging_company = fields.Many2one('res.partner', string='Empresa Jalonadora')
    x_acceptance_data_policy = fields.Boolean(string='Acepta política de tratamiento de datos')
    x_acceptance_date = fields.Date(string='Fecha de aceptación')
    x_not_contacted_again = fields.Boolean(string='No volver a ser contactado')
    x_reason_desvinculation = fields.Selection([
                                        ('1', 'Desvinculado por no pago'), 
                                        ('2', 'Desvinculado Voluntariamente'), 
                                        ('3', 'Desvinculado por Cesión y/o Fusión'),
                                        ('4', 'Desvinculado por Liquidación de la Empresa'),
                                        ('5', 'Desvinculado por mal uso del sistema')
                                    ], string='Desvinculado por')
  
    #INFORMACION FINANCIERA
    x_asset_range = fields.Selection([
                                        ('01', 'DE 0 A 9.9'), 
                                        ('02', 'DE 10 A 24.9'), 
                                        ('03', 'DE 25 A 49.9'),
                                        ('04', 'DE 50 A 99.9'),
                                        ('05', 'DE 100 A 249.9'),
                                        ('06', 'DE 250 A 499.9'),
                                        ('07', 'DE 500 A 749.9'),
                                        ('08', 'DE 750 A 999.9'),
                                        ('09', 'DE 1,000 A 2,499.9'),
                                        ('10', 'DE 2,500 A 4,999.9'),
                                        ('11', 'DE 5,000 A 9,999.9'),
                                        ('12', 'DE 10,000 A 49,999.9'),
                                        ('13', 'DE 50,000 A 99,999.9'),
                                        ('14', 'DE 100,000 A 249,999.9'),
                                        ('15', 'DE 250,000 A 499,999.9'),
                                        ('16', 'DE 500,000 A 999,999.9'),
                                        ('17', 'MAS DE 1,000,000')                                        
                                    ], string='Rango de Activos')
    x_income_range = fields.Selection([
                                        ('01', 'DE 0 A 9.9'), 
                                        ('02', 'DE 10 A 24.9'), 
                                        ('03', 'DE 25 A 49.9'),
                                        ('04', 'DE 50 A 99.9'),
                                        ('05', 'DE 100 A 249.9'),
                                        ('06', 'DE 250 A 499.9'),
                                        ('07', 'DE 500 A 749.9'),
                                        ('08', 'DE 750 A 999.9'),
                                        ('09', 'DE 1,000 A 2,499.9'),
                                        ('10', 'DE 2,500 A 4,999.9'),
                                        ('11', 'DE 5,000 A 9,999.9'),
                                        ('12', 'DE 10,000 A 49,999.9'),
                                        ('13', 'DE 50,000 A 99,999.9'),
                                        ('14', 'DE 100,000 A 249,999.9'),
                                        ('15', 'DE 250,000 A 499,999.9'),
                                        ('16', 'DE 500,000 A 999,999.9'),
                                        ('17', 'MAS DE 1,000,000')                                          
                                    ], string='Rango de Ingresos')
    x_date_update_asset = fields.Date(string='Fecha de última modificación', compute='_date_update_asset', store=True)
    x_company_size = fields.Selection([
                                        ('01', 'Mipyme'), 
                                        ('02', 'Pyme'), 
                                        ('03', 'Mediana'),
                                        ('04', 'Grande')                                        
                                    ], string='Tamaño empresa')

    #INFORMACION TRIBUTARIA
    x_tax_responsibilities = fields.Many2many('testlogyca.responsibilities_rut', string='Responsabilidades Tributarias')

    #INFORMACION COMERCIAL
    x_account_origin = fields.Selection([
                                        ('01', 'Campañas'), 
                                        ('02', 'Eventos'), 
                                        ('03', 'Referenciado'),
                                        ('04', 'Telemercadeo'),
                                        ('05', 'Web'),
                                        ('06', 'Otro')                                      
                                    ], string='Origen de la cuenta')
    x_member_id_team = fields.Many2one('res.users', string='Propietario de la cuenta')
    x_additional_codes  = fields.Boolean(string='¿Maneja Códigos Adicionales?')    
    x_codes_gtin = fields.Boolean(string='¿Maneja Códigos GTIN-8?')
    
    #INFORMACIÓN CONTACTO
    x_contact_type = fields.Many2many('testlogyca.contact_types', string='Tipo de contacto')
    x_contact_job_title = fields.Many2one('testlogyca.job_title', string='Cargo')
    x_contact_area = fields.Many2one('testlogyca.areas', string='Área')

    #INFORMACION FACTURACION ELECTRÓNICA
    x_email_contact_invoice_electronic = fields.Char(string='Correo electrónico contacto')
    x_name_contact_invoice_electronic = fields.Char(string='Nombre contacto')
    x_phone_contact_invoice_electronic = fields.Char(string='Telefono contacto')
    x_city_contact_invoice_electronic = fields.Char(string='Ciudad contacto')
    x_area_contact_invoice_electronic = fields.Char(string='Área contacto')
    x_position_contact_invoice_electronic = fields.Char(string='Cargo contacto')
    x_email_invoice_electronic = fields.Char(string='Correo electrónico para recepción electrónica de facturas')
    
    @api.depends('x_asset_range')
    def _date_update_asset(self):
        self.x_date_update_asset = fields.Date.today()

class ResCountry(models.Model):
    _inherit = 'res.country'
	
    x_code_dian = fields.Char(string='Código del país para la DIAN')

class ResCountryState(models.Model):
    _inherit = 'res.country.state'
	
    x_code_dian = fields.Char(string='Código de provincia/departamento para la DIAN')