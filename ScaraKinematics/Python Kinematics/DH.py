# Created by John Steele 2017

@mfunction("rotMat")
def DH(basic=None, jnt=None):
    #
    # Objective:
    #
    # Generate the Denavit-Hartenberg homogeneous rotational matrix for a given
    # joint, provided a complete DH Parameters table
    # _________________________________________________________________________
    #
    # Input:
    #
    # basic: Table of defined DH Parameters of size n by 4
    # jnt: The desired end point to be defined by rotMat
    #
    # Output:
    #
    # rotMat: DH homogeneous rotational matrix of joint jnt
    # _________________________________________________________________________
    # 
    # Define:
    #
    # a_i: Link length about the x-axis at a given moment in time
    # d_i: Link length about the z-axis at a given moment in time
    # p_i: Joint orientation about the x-axis at a given moment in time
    # t_i: Joint orientation about the z-axis at a given moment in time
    #
    # s: Size of basic
    # n: The row size of basic
    # i: Current joint of discussion
    # _________________________________________________________________________
    #
    # Assume/State:
    # 
    # - 'basic' must be size n by 4, where n > 4.
    # - 'jnt' must be and integer within the range [1 n].
    # - A given variable in basic must be numeric.  If not, assign zero.
    # _________________________________________________________________________

    # Check for input errors

    s = size(basic)

    if (s(1) <= 1 or s(2) != 4):
        error(mstring('Paramater Array has incorrect dimensions.'))
        end

        n = s(1)

        if (jnt < 1 or jnt > n):
            error(mstring('User specified nonexistant joint.'))
            end

            # Initialize rotMat
            rotMat = 1

            # Loop through matrices utilizing table rows, until the desired joint has
            # been reached
            for i in mslice[1:jnt]:

                a = basic(i, 1)            # a_i
                d = basic(i, 2)            # d_i
                p = basic(i, 3)            # alpha_i
                t = basic(i, 4)            # theda_i




                dh_i = mcat([cosd(t) - sind(t) * cosd(p), sind(t) * sind(p), a * cosd(t), OMPCSEMI, sind(t), cosd(t) * cosd(p) - cosd(t) * sind(p), a * sind(t), OMPCSEMI, 0, sind(p), cosd(p), d, OMPCSEMI, 0, 0, 0, 1])

                rotMat = rotMat * dh_i
                end

                end