import bpy
from mathutils import Vector

#Basic Info
bl_info = {
    "name": "Floor Snap Tool",
    "author": "Chris Nendick",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N-panel",
    "description": "Snaps selected object to the floor",
    "category": "Object"
}

#new operator for snapping objects to the floor.
class OBJECT_OT_snap_to_floor(bpy.types.Operator):
    bl_idname = "object.snap_to_floor"
    bl_label = "Floor Snap Tool"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Execute operator
    def execute(self, context):
        
        obj = context.active_object 
        if obj is None:
            self.report({'ERROR'}, "No object selected")  
            return {'CANCELLED'}
        
        # Calculate the world coordinates of the bounding box.
        bbox = [obj.matrix_world @ Vector(v) for v in obj.bound_box]  
        
        #Find the minimum Z value from the bounding box.
        min_z = min(v.z for v in bbox)  
        
        #Create an offset to snap the object to the floor.
        offset = Vector((0, 0, -min_z)) 
         
        # Apply the offset to the object's location.
        obj.location += offset  
        
        return {'FINISHED'} 

#Panel creation
class OBJECT_PT_snap_to_floor_panel(bpy.types.Panel):
    bl_label = "Snap to Floor"
    bl_idname = "OBJECT_PT_snap_to_floor_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Floor Snap"
    
    #Panel Layout
    def draw(self, context):
        layout = self.layout
        layout.operator("object.snap_to_floor", text="Snap to Floor")  

# Register the operator and panel
def register():
    bpy.utils.register_class(OBJECT_OT_snap_to_floor)
    bpy.utils.register_class(OBJECT_PT_snap_to_floor_panel)

# Unregister the operator and panel
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_snap_to_floor)
    bpy.utils.unregister_class(OBJECT_PT_snap_to_floor_panel)


if __name__ == "__main__":
    register()
