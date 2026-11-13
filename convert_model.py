"""Export the downloaded scene with transforms applied, preserving source scale."""
from pathlib import Path
import json
import numpy as np
import trimesh


def convert(glb):
    glb = Path(glb)
    mesh = trimesh.load_scene(glb).to_mesh()
    if not len(mesh.faces) or not np.isfinite(mesh.vertices).all():
        raise ValueError('Model has no triangles or contains invalid coordinates')
    mesh.merge_vertices(merge_tex=True, merge_norm=True)
    mesh.update_faces(mesh.unique_faces())
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.remove_unreferenced_vertices()
    mesh.export(glb.with_suffix('.stl'))
    mesh.export(glb.with_suffix('.obj'), include_texture=False)
    _, counts = np.unique(mesh.edges_sorted, axis=0, return_counts=True)
    report = {
        'triangles': len(mesh.faces), 'vertices': len(mesh.vertices),
        'dimensions_source_units': mesh.extents.tolist(),
        'watertight': bool(mesh.is_watertight),
        'consistent_winding': bool(mesh.is_winding_consistent),
        'boundary_edges': int((counts == 1).sum()),
        'nonmanifold_edges': int((counts > 2).sum()),
        'scale_note': 'Coordinates are preserved. STL has no unit metadata. Confirm dimensions in your slicer.',
        'print_note': 'Open edges, intersections and wall thickness may need repair. No automatic hole filling or remeshing was applied.',
    }
    glb.with_name('mesh-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    import sys
    print(json.dumps(convert(sys.argv[1]), indent=2))
