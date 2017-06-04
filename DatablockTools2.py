bl_info = {
	"name": "Datablock Tools",
	"author": "Vitor Balbio, Mackenzie Crawford",
	"version": (2, 0),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Datablock Tools",
	"description": "Some tools to handle Datablocks",
	"warning": "",
	"tracker_url": "",
	"category": "3D View"}
	
import bpy
import os
import re

class CleanImagesOP(bpy.types.Operator):
	#Replace the ".0x" images with the original and mark this to remove in next load
	bl_idname = "object.clean_images"
	bl_label = "Clean Images Datablock"

	@classmethod
	def poll(cls, context):
		return context.selected_objects is not None

	def execute(self, context):
		ImageList = []
		#if the last character is not a number then remove the last 3 characters (image format extension)
		for i in bpy.data.images:
			try:
				a = int(i.name[-1])
				imagename = i.name
			except ValueError:
				imagename, a = os.path.splitext(i.name)

		ImageList.append([imagename,i])

		for obj in bpy.context.selected_objects:
			for uv in obj.data.uv_textures.items():
				for faceTex in uv[1].data:
					image = faceTex.image          
					#if the last character is not number then removes the last 3 characters ( image format)
					try:
						a = int(image.name[-1])
						imagename = image.name
					except ValueError:
						imagename, a = os.path.splitext(image.name)

					if(".0" in imagename):
						for ima_name, ima in ImageList:
							if((ima_name == imagename.split(".")[0]) and (not bool(re.search(r'\.\(\d){3}', ima_name)))):
								faceTex.image.user_clear()
								faceTex.image = ima
		return {'FINISHED'}

class CleanMaterialsOP(bpy.types.Operator):
	#Replace the ".0x" materials with the original and mark this to remove in next load
	bl_idname = "object.clean_materials"
	bl_label = "Clean Materials Datablock"

	@classmethod
	def poll(cls, context):
		return context.selected_objects is not None

	def execute(self, context):
		matlist = bpy.data.materials
		for obj in bpy.context.selected_objects:
			for mat_slt in obj.material_slots:
				if(mat_slt.material != None and bool(re.search(r'\.(\d){3}', mat_slt.material.name))): #if a material is set, and its name contains a . followed by 3 digits
					replaced = False
					for mat in matlist:
						if((mat.name == mat_slt.material.name.split(".")[0]) and (not bool(re.search(r'\.(\d){3}', mat.name)))):
							mat_slt.material = mat
							replaced = True
					if replaced == False: #We found no "original" material, so we just rename this one
						mat_slt.material.name = mat_slt.material.name.split(".")[0]
		return {'FINISHED'}

class SetInstanceOP(bpy.types.Operator):
	#Set all Selected Objects as instance of Active Object
	bl_idname = "object.set_instance"
	bl_label = "Set as Instance"

	@classmethod
	def poll(cls, context):
		return ((context.selected_objects is not None) and (context.active_object is not None))

	def execute(self, context):
		active_obj = bpy.context.active_object
		for sel_obj in bpy.context.selected_objects:
			sel_obj.data = active_obj.data
		return {'FINISHED'}

class DatablockToolsMenu(bpy.types.Menu):
	bl_label = "Datablock Tools"
	bl_idname = "VIEW_MT_datablock_tools"

	def draw(self, context):
		layout = self.layout

		layout.operator("object.clean_images")
		layout.operator("object.clean_materials")
		layout.operator("object.set_instance")

def draw_item(self, context):
	layout = self.layout
	layout.menu(DatablockToolsMenu.bl_idname)

def register():
	bpy.utils.register_class(CleanImagesOP)
	bpy.utils.register_class(CleanMaterialsOP)
	bpy.utils.register_class(SetInstanceOP)
	bpy.utils.register_class(DatablockToolsMenu)

	# lets add ourselves to the main header
	bpy.types.VIEW3D_MT_object.append(draw_item)

def unregister():
	bpy.utils.register_class(CleanImagesOP)
	bpy.utils.unregister_class(CleanMaterialsOP)
	bpy.utils.unregister_class(SetInstanceOP)
	bpy.utils.unregister_class(DatablockToolsMenu)

	bpy.types.VIEW3D_MT_object.remove(draw_item)

if __name__ == "__main__":
	register()