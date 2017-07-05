def hierarchy_permit(author, target):
    top_author_role = author.top_role.position
    top_target_role = target.top_role.position
    return top_author_role > top_target_role
