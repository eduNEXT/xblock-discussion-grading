Discussion Grading XBlock
#########################

|status-badge| |license-badge| |ci-badge|

Purpose
*******

Allows course authors to create a gradable component that will assign a
grade to students based on their participation in the discussion forum.
The instructor will be able to choose between different grading methods
and configure each of them.

This XBlock has been created as an open source contribution to the Open
edX platform and has been funded by **Unidigital** project from the Spanish
Government - 2023.


Enabling the XBlock in a course
*******************************

Once the XBlock has been installed in your Open edX installation, you can
enable it in a course from Studio through the **Advanced Settings**.

1. Go to Studio and open the course to which you want to add the XBlock.
2. Go to **Settings** > **Advanced Settings** from the top menu.
3. Search for **Advanced Module List** and add ``"discussion_grading"``
   to the list.
4. Click **Save Changes** button.


Adding a Discussion Grading Component to a course unit
*********************************************************

From Studio, you can add the Discussion Grading Component to a course unit.

1. Click on the **Advanced** button in **Add New Component**.

   .. image:: https://github.com/eduNEXT/xblock-discussion-grading/assets/64033729/f86c859f-707d-48a3-aa8d-b16f10d1f84c
      :alt: Open Advanced Components

2. Select **Discussion Grading** from the list.

   .. image:: https://github.com/eduNEXT/xblock-discussion-grading/assets/64033729/30a09d1c-e6b0-41fd-9c63-026c126c6055
      :alt: Select Discussion Grading Component

3. Configure the component as needed.


View from the Learning Management System (CMS)
**********************************************

The **Discussion Grading** component has a set of settings that can be
configured by the course author.

.. image:: https://github.com/eduNEXT/xblock-discussion-grading/assets/64033729/6baaa669-f975-4155-a1d1-dee25fbeddc7
    :alt: Settings for the Discussion Grading component

The **Discussion Grading** component has the following settings:

- **Grading Method**: Allow the course author to choose between different
  grading methods. The available options are:
  - **Minimum Participations**: The learner will receive the maximum grade
    if they have the minimum number of participations in the discussion
    forum. If the learner does not have the minimum number of
    participations, the grade is 0
  - **Average Participations**: The learner will receive a grade based on
    the average number of participations in the discussion forum. The grade
    will be calculated as: (learner_participations / number of
    participations).
- **Maximum Attempts**: Allows the course author to set the maximum number of
  attempts that a learner can calculate the grade. If no value is set, the
  learner can calculate the grade as many times as they want.
- **Number of Participations**: Allows the course author to set the number of
  participations that the learner must have in the discussion forum to receive
  the maximum grade.
- **Problem Weight**: Allows the course author to set the weight of the
  discussion grading component in the final grade of the course.
- **Instructions Text**: Allows the course author to set the instructions that
  will be displayed to the learner.
- **Button Text**: Allows the course author to set the text that will be
  displayed on the button that the learner will use to calculate the grade.


View from the Learning Management System (LMS)
**********************************************

When a learner accesses the course, they will see the instructions and the
button to calculate the grade. If the course author has set the maximum
number of attempts, the learner will see the number of attempts left. After
the learner has calculated the grade, they will see the grade obtained.

.. image:: https://github.com/eduNEXT/xblock-discussion-grading/assets/64033729/33b0f331-3554-4b2a-bb81-a2ddf0a02b9a
    :alt: View of the component in the LMS


Experimenting with this XBlock in the Workbench
************************************************

`XBlock`_ is the Open edX component architecture for building custom learning
interactive components.

You can see the Discussion Grading component in action in the XBlock
Workbench. Running the Workbench requires having docker running.

.. code::

    git clone git@github.com:eduNEXT/xblock-discussion-grading
    virtualenv venv/
    source venv/bin/activate
    cd xblock-discussion-grading
    make upgrade
    make install
    make dev.run

Once the process is done, you can interact with the Discussion Grading
XBlock in the Workbench by navigating to http://localhost:8000

For details regarding how to deploy this or any other XBlock in the Open edX
platform, see the `installing-the-xblock`_ documentation.

.. _XBlock: https://openedx.org/r/xblock
.. _installing-the-xblock: https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock

Getting Help
*************

If you're having trouble, the Open edX community has active discussion forums
available at https://discuss.openedx.org where you can connect with others in
the community.

Also, real-time conversations are always happening on the Open edX community
Slack channel. You can request a `Slack invitation`_, then join the
`community Slack workspace`_.

For anything non-trivial, the best path is to open an `issue`_ in this
repository with as many details about the issue you are facing as you can
provide.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _issue: https://github.com/eduNEXT/xblock-discussion-grading/issues
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL-3.0 unless otherwise
noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.


Translations
============

This Xblock is initially available in English and Spanish. You can help by
translating this component to other languages. Follow the steps below:

1. Create a folder for the translations in ``locale/``, eg:
   ``locale/fr_FR/LC_MESSAGES/``, and create your ``text.po``
   file with all the translations.
2. Run ``make compile_translations``, this will generate the ``.mo`` file.
3. Create a pull request with your changes.


Reporting Security Issues
*************************

Please do not report a potential security issue in public. Please email
security@edunext.co.


.. |ci-badge| image:: https://github.com/eduNEXT/xblock-discussion-grading/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/eduNEXT/xblock-discussion-grading/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/xblock-discussion-grading.svg
    :target: https://github.com/eduNEXT/xblock-discussion-grading/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
