bl_info = {
	"name": "Datablock Tools",
	"author": "Mackenzie Crawford, Vitor Balbio",
	"version": (2, 1),
	"blender": (2, 79, 0),
	"location": "View3D > Object > Datablock Tools",
	"description": "Some tools to handle datablocks",
	"warning": "",
	"tracker_url": "",
	"category": "3D View"}
	
import bpy
import os
import re

class CleanImagesOP(bpy.types.Operator):
	#replace the ".0x" images with the original and mark this to remove in next load
	bl_idname = "object.clean_images"
	bl_label = "Clean Images Datablocks"
	
	@classmethod
	def poll(cls, context):
		return context.selected_objects is not None

	def execute(self, context):
		ImageList = []
		#get full image name including extension
		for i in bpy.data.images:
			ImageList.append([i.name,i])

		for obj in bpy.context.selected_objects:
			for uv in obj.data.uv_textures.items():
				for faceTex in uv[1].data:
					if (not (faceTex.image is None)):
						image = faceTex.image

						if (bool(re.search(r'\.(\d){3}', image.name))): #if an image is set, and its name contains a . followed by 3 digits
							replaced = False
							for ima_name, ima in ImageList:
								if (image.name.startswith(ima_name) and (".0" not in ima_name)):
									faceTex.image.user_clear()
									faceTex.image = ima
									replaced = True
							if (replaced == False):
								#we didn't find a match, rename this one
								image.name = image.name.rsplit(".", 1)[0] #splits on the last . in the image name and returns the left part. Allows handling of names with multiple .s
		return {'FINISHED'}
		
class CleanMaterialsOP(bpy.types.Operator):
	#replace the ".0x" materials with the original and mark this to remove in next load
	bl_idname = "object.clean_materials"
	bl_label = "Clean Materials Datablocks"

	@classmethod
	def poll(cls, context):
		return context.selected_objects is not None

	def execute(self, context):
		matlist = bpy.data.materials
		for obj in bpy.context.selected_objects:
			for mat_slt in obj.material_slots:
				if (mat_slt.material != None and bool(re.search(r'\.(\d){3}', mat_slt.material.name))): #if a material is set, and its name contains a . followed by 3 digits
					replaced = False
					for mat in matlist:
						if ((mat.name == mat_slt.material.name.rsplit(".", 1)[0]) and (not bool(re.search(r'\.(\d){3}', mat.name)))):
							mat_slt.material = mat
							replaced = True
					if replaced == False:
						#we didn't find a match, rename this one
						mat_slt.material.name = mat_slt.material.name.rsplit(".", 1)[0] #splits on the last . in the material name and returns the left part. Allows handling of names with multiple .s
		return {'FINISHED'}
		
class RemoveAllMaterialsOP(bpy.types.Operator):
	#removes all materials from selected objects
	bl_idname = "object.remove_materials"
	bl_label = "Remove All Materials Datablocks"

	@classmethod
	def poll(cls, context):
		return context.selected_objects is not None
		
	def execute(self, context):
		for obj in bpy.context.selected_objects:
			#iterate through materials list and remove each sequentially
			obj.active_material_index = 0
			for i in range(len(obj.material_slots)):
				bpy.ops.object.material_slot_remove({'object': obj})
		return {'FINISHED'}

class SetInstanceOP(bpy.types.Operator):
	#set all selected objects as instance of active object
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

		layout.operator("object.clean_materials")
		layout.operator("object.remove_materials")
		layout.operator("object.clean_images")
		layout.operator("object.set_instance")

def draw_item(self, context):
	layout = self.layout
	layout.menu(DatablockToolsMenu.bl_idname)

def register():
	bpy.utils.register_class(CleanMaterialsOP)
	bpy.utils.register_class(RemoveAllMaterialsOP)
	bpy.utils.register_class(CleanImagesOP)
	bpy.utils.register_class(SetInstanceOP)
	bpy.utils.register_class(DatablockToolsMenu)

	# lets add ourselves to the main header
	bpy.types.VIEW3D_MT_object.append(draw_item)

def unregister():
	bpy.utils.unregister_class(CleanMaterialsOP)
	bpy.utils.unregister_class(RemoveAllMaterialsOP)
	bpy.utils.register_class(CleanImagesOP)
	bpy.utils.unregister_class(SetInstanceOP)
	bpy.utils.unregister_class(DatablockToolsMenu)

	bpy.types.VIEW3D_MT_object.remove(draw_item)

if __name__ == "__main__":
	register()