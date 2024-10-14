transform = ergasia2.Transform()



transform.rotate(theta, rot_axis_0)
transform.translate(t_0)
transform.translate(t_1)
transformed_points=transform.transform_pts(v_pos)